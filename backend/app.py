from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import secrets
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)


# Try to import bcrypt, but make it optional
try:
    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt(app)
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    print("Warning: bcrypt not available. User authentication features will be disabled.")

# Database configuration - using SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), 'quick_poll_db.sqlite')

def get_db_connection():
    """Create and return database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable dictionary-like access
    return conn

def init_database():
    """Initialize database and create tables if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL
        )
    """)
    
    # Create polls table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS polls (
            poll_id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator_id INTEGER,
            question VARCHAR(255) NOT NULL,
            poll_link VARCHAR(20) NOT NULL UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    """)
    
    # Create options table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS options (
            option_id INTEGER PRIMARY KEY AUTOINCREMENT,
            poll_id INTEGER NOT NULL,
            option_text VARCHAR(255) NOT NULL,
            FOREIGN KEY (poll_id) REFERENCES polls(poll_id) ON DELETE CASCADE
        )
    """)
    
    # Create votes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
            poll_id INTEGER NOT NULL,
            voter_id INTEGER,
            option_id INTEGER NOT NULL,
            voted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (poll_id) REFERENCES polls(poll_id) ON DELETE CASCADE,
            FOREIGN KEY (voter_id) REFERENCES users(user_id) ON DELETE SET NULL,
            FOREIGN KEY (option_id) REFERENCES options(option_id) ON DELETE CASCADE,
            UNIQUE(voter_id, poll_id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Initialize database on startup
init_database()

def generate_poll_link():
    """Generate unique poll link"""
    return secrets.token_urlsafe(10)[:20]

def row_to_dict(row):
    """Convert SQLite Row to dictionary"""
    if row is None:
        return None
    return dict(row)

# ============= USER ENDPOINTS =============

@app.route('/api/users/register', methods=['POST'])
def register_user():
    """Register a new user"""
    if not BCRYPT_AVAILABLE:
        return jsonify({'error': 'User authentication not available. bcrypt is not installed.'}), 503
    
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'error': 'All fields are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Email already registered'}), 400
        
        # Hash password
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Insert user
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        
        conn.close()
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id
        }), 201
        
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/login', methods=['POST'])
def login_user():
    """Login user"""
    if not BCRYPT_AVAILABLE:
        return jsonify({'error': 'User authentication not available. bcrypt is not installed.'}), 503
    
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            user = row_to_dict(row)
            if bcrypt.check_password_hash(user['password_hash'], password):
                return jsonify({
                    'message': 'Login successful',
                    'user': {
                        'user_id': user['user_id'],
                        'username': user['username'],
                        'email': user['email']
                    }
                }), 200
        
        return jsonify({'error': 'Invalid email or password'}), 401
            
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# ============= POLL ENDPOINTS =============

@app.route('/api/polls', methods=['POST'])
def create_poll():
    """Create a new poll with options"""
    try:
        data = request.get_json()
        question = data.get('question')
        options = data.get('options', [])
        creator_id = data.get('creator_id')  # Optional, can be None for anonymous
        
        if not question:
            return jsonify({'error': 'Poll question is required'}), 400
        
        if not options or len(options) < 2:
            return jsonify({'error': 'At least 2 options are required'}), 400
        
        # Validate option texts
        valid_options = [opt.strip() for opt in options if opt.strip()]
        if len(valid_options) < 2:
            return jsonify({'error': 'At least 2 valid options are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Generate unique poll link
        poll_link = generate_poll_link()
        
        # Check if poll_link already exists (very unlikely, but check anyway)
        while True:
            cursor.execute("SELECT poll_id FROM polls WHERE poll_link = ?", (poll_link,))
            if not cursor.fetchone():
                break
            poll_link = generate_poll_link()
        
        # Insert poll
        cursor.execute(
            "INSERT INTO polls (creator_id, question, poll_link) VALUES (?, ?, ?)",
            (creator_id if creator_id else None, question, poll_link)
        )
        poll_id = cursor.lastrowid
        
        # Insert options
        for option_text in valid_options:
            cursor.execute(
                "INSERT INTO options (poll_id, option_text) VALUES (?, ?)",
                (poll_id, option_text)
            )
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Poll created successfully',
            'poll_id': poll_id,
            'poll_link': poll_link
        }), 201
        
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/polls/<poll_link>', methods=['GET'])
def get_poll(poll_link):
    """Get poll details with options"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get poll
        cursor.execute("SELECT * FROM polls WHERE poll_link = ?", (poll_link,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({'error': 'Poll not found'}), 404
        
        poll = row_to_dict(row)
        
        # Get options
        cursor.execute(
            "SELECT option_id, option_text FROM options WHERE poll_id = ?",
            (poll['poll_id'],)
        )
        option_rows = cursor.fetchall()
        options = [row_to_dict(row) for row in option_rows]
        
        # Get vote counts for each option
        for option in options:
            cursor.execute(
                "SELECT COUNT(*) as vote_count FROM votes WHERE option_id = ?",
                (option['option_id'],)
            )
            vote_result = cursor.fetchone()
            option['vote_count'] = vote_result[0] if vote_result else 0
        
        conn.close()
        
        # Convert datetime to ISO format string
        created_at = poll.get('created_at')
        if created_at and isinstance(created_at, str):
            created_at = created_at
        elif created_at:
            created_at = created_at.isoformat() if hasattr(created_at, 'isoformat') else str(created_at)
        
        return jsonify({
            'poll': {
                'poll_id': poll['poll_id'],
                'question': poll['question'],
                'poll_link': poll['poll_link'],
                'created_at': created_at,
                'options': options
            }
        }), 200
        
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/polls', methods=['GET'])
def get_all_polls():
    """Get all polls (optional endpoint)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM polls ORDER BY created_at DESC")
        poll_rows = cursor.fetchall()
        polls = [row_to_dict(row) for row in poll_rows]
        
        # Get options for each poll
        for poll in polls:
            cursor.execute(
                "SELECT option_id, option_text FROM options WHERE poll_id = ?",
                (poll['poll_id'],)
            )
            option_rows = cursor.fetchall()
            poll['options'] = [row_to_dict(row) for row in option_rows]
        
        conn.close()
        
        return jsonify({'polls': polls}), 200
        
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# ============= VOTE ENDPOINTS =============

@app.route('/api/votes', methods=['POST'])
def submit_vote():
    """Submit a vote for a poll option"""
    try:
        data = request.get_json()
        poll_id = data.get('poll_id')
        option_id = data.get('option_id')
        voter_id = data.get('voter_id')  # Optional, can be None for anonymous
        
        if not poll_id or not option_id:
            return jsonify({'error': 'Poll ID and option ID are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify option belongs to poll
        cursor.execute(
            "SELECT poll_id FROM options WHERE option_id = ?",
            (option_id,)
        )
        option = cursor.fetchone()
        
        if not option or option[0] != poll_id:
            conn.close()
            return jsonify({'error': 'Invalid option for this poll'}), 400
        
        # Check if user already voted (only if voter_id provided)
        if voter_id:
            cursor.execute(
                "SELECT vote_id FROM votes WHERE voter_id = ? AND poll_id = ?",
                (voter_id, poll_id)
            )
            if cursor.fetchone():
                conn.close()
                return jsonify({'error': 'You have already voted on this poll'}), 400
        
        # Insert vote
        try:
            cursor.execute(
                "INSERT INTO votes (poll_id, voter_id, option_id) VALUES (?, ?, ?)",
                (poll_id, voter_id if voter_id else None, option_id)
            )
            conn.commit()
            vote_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'You have already voted on this poll'}), 400
        
        conn.close()
        
        return jsonify({
            'message': 'Vote submitted successfully',
            'vote_id': vote_id
        }), 201
        
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/polls/<poll_link>/results', methods=['GET'])
def get_poll_results(poll_link):
    """Get poll results with vote counts"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get poll
        cursor.execute("SELECT * FROM polls WHERE poll_link = ?", (poll_link,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({'error': 'Poll not found'}), 404
        
        poll = row_to_dict(row)
        
        # Get options with vote counts
        cursor.execute("""
            SELECT o.option_id, o.option_text, COUNT(v.vote_id) as vote_count
            FROM options o
            LEFT JOIN votes v ON o.option_id = v.option_id
            WHERE o.poll_id = ?
            GROUP BY o.option_id, o.option_text
            ORDER BY o.option_id
        """, (poll['poll_id'],))
        option_rows = cursor.fetchall()
        options = [row_to_dict(row) for row in option_rows]
        
        # Calculate total votes
        total_votes = sum(option['vote_count'] for option in options)
        
        # Add percentage for each option
        for option in options:
            option['percentage'] = round(
                (option['vote_count'] / total_votes * 100) if total_votes > 0 else 0, 
                2
            )
        
        conn.close()
        
        # Convert datetime to ISO format string
        created_at = poll.get('created_at')
        if created_at and isinstance(created_at, str):
            created_at = created_at
        elif created_at:
            created_at = created_at.isoformat() if hasattr(created_at, 'isoformat') else str(created_at)
        
        return jsonify({
            'poll': {
                'poll_id': poll['poll_id'],
                'question': poll['question'],
                'poll_link': poll['poll_link'],
                'created_at': created_at,
                'total_votes': total_votes,
                'options': options
            }
        }), 200
        
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Quick Poll App - Backend Server")
    print("=" * 50)
    print(f"Database: {DB_PATH}")
    print("Starting server on http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
