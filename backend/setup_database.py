"""Script to set up and test database connection"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': int(os.getenv('DB_PORT', 3306))
}

def test_connection():
    """Test MySQL connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Successfully connected to MySQL server")
            return connection
    except Error as e:
        print(f"Connection failed: {e}")
        return None

def create_database(connection):
    """Create database if it doesn't exist"""
    db_name = os.getenv('DB_NAME', 'quick_poll_db')
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' is ready")
        cursor.close()
        return True
    except Error as e:
        print(f"Failed to create database: {e}")
        return False

def read_sql_file(file_path):
    """Read SQL file and split into individual statements"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove comments and split by semicolons
    statements = []
    current_statement = ""
    
    for line in content.split('\n'):
        # Skip comment lines
        if line.strip().startswith('--') or line.strip().startswith('/*'):
            continue
        current_statement += line + '\n'
    
    # Split by semicolons but keep complete statements
    statements = [s.strip() for s in current_statement.split(';') if s.strip() and not s.strip().startswith('/*')]
    return statements

def setup_schema(connection):
    """Import schema from SQL file"""
    db_name = os.getenv('DB_NAME', 'quick_poll_db')
    schema_file = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
    
    try:
        cursor = connection.cursor()
        cursor.execute(f"USE {db_name}")
        
        # Read and execute schema file
        if os.path.exists(schema_file):
            print(f"Reading schema from: {schema_file}")
            with open(schema_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Execute statements one by one
            statements = []
            current = ""
            for line in sql_content.split('\n'):
                # Skip comment-only lines
                stripped = line.strip()
                if stripped.startswith('--') or stripped.startswith('/*') or not stripped:
                    continue
                current += line + '\n'
                if stripped.endswith(';'):
                    statements.append(current.strip())
                    current = ""
            
            if current.strip():
                statements.append(current.strip())
            
            # Execute each statement
            for statement in statements:
                if statement and not statement.startswith('SET') and not statement.startswith('START') and not statement.startswith('COMMIT'):
                    try:
                        cursor.execute(statement)
                    except Error as e:
                        # Ignore "already exists" errors
                        if 'already exists' not in str(e).lower() and 'duplicate' not in str(e).lower():
                            print(f"  Warning: {str(e)[:100]}")
            
            connection.commit()
            print("Database schema imported successfully")
            
            # Verify tables exist
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"Found {len(tables)} tables: {[t[0] for t in tables]}")
        else:
            print(f"Schema file not found at: {schema_file}")
            print("  Creating tables manually...")
            create_tables_manually(cursor)
            connection.commit()
        
        cursor.close()
        return True
    except Error as e:
        print(f"Failed to setup schema: {e}")
        return False

def create_tables_manually(cursor):
    """Create tables manually if schema file is not available"""
    tables = [
        """CREATE TABLE IF NOT EXISTS `users` (
          `user_id` int(11) NOT NULL AUTO_INCREMENT,
          `username` varchar(50) NOT NULL,
          `email` varchar(100) NOT NULL,
          `password_hash` varchar(255) NOT NULL,
          PRIMARY KEY (`user_id`),
          UNIQUE KEY `email` (`email`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci""",
        
        """CREATE TABLE IF NOT EXISTS `polls` (
          `poll_id` int(11) NOT NULL AUTO_INCREMENT,
          `creator_id` int(11) DEFAULT NULL,
          `question` varchar(255) NOT NULL,
          `poll_link` varchar(20) NOT NULL,
          `created_at` datetime DEFAULT current_timestamp(),
          PRIMARY KEY (`poll_id`),
          UNIQUE KEY `poll_link` (`poll_link`),
          KEY `creator_id` (`creator_id`),
          CONSTRAINT `polls_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci""",
        
        """CREATE TABLE IF NOT EXISTS `options` (
          `option_id` int(11) NOT NULL AUTO_INCREMENT,
          `poll_id` int(11) NOT NULL,
          `option_text` varchar(255) NOT NULL,
          PRIMARY KEY (`option_id`),
          KEY `poll_id` (`poll_id`),
          CONSTRAINT `options_ibfk_1` FOREIGN KEY (`poll_id`) REFERENCES `polls` (`poll_id`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci""",
        
        """CREATE TABLE IF NOT EXISTS `votes` (
          `vote_id` int(11) NOT NULL AUTO_INCREMENT,
          `poll_id` int(11) NOT NULL,
          `voter_id` int(11) DEFAULT NULL,
          `option_id` int(11) NOT NULL,
          `voted_at` datetime DEFAULT current_timestamp(),
          PRIMARY KEY (`vote_id`),
          UNIQUE KEY `unique_vote` (`voter_id`,`poll_id`),
          KEY `fk_votes_poll` (`poll_id`),
          KEY `fk_votes_option` (`option_id`),
          CONSTRAINT `fk_votes_option` FOREIGN KEY (`option_id`) REFERENCES `options` (`option_id`) ON DELETE CASCADE ON UPDATE CASCADE,
          CONSTRAINT `fk_votes_poll` FOREIGN KEY (`poll_id`) REFERENCES `polls` (`poll_id`) ON DELETE CASCADE ON UPDATE CASCADE,
          CONSTRAINT `fk_votes_voter` FOREIGN KEY (`voter_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"""
    ]
    
    for table_sql in tables:
        try:
            cursor.execute(table_sql)
        except Error as e:
            if 'already exists' not in str(e).lower():
                print(f"  Warning creating table: {str(e)[:100]}")

def test_database_connection():
    """Test connection to the actual database"""
    db_name = os.getenv('DB_NAME', 'quick_poll_db')
    config = {**DB_CONFIG, 'database': db_name}
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print(f"Successfully connected to database '{db_name}'")
            connection.close()
            return True
    except Error as e:
        print(f"Failed to connect to database: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Database Setup Script")
    print("=" * 50)
    print()
    
    print("Step 1: Testing MySQL connection...")
    connection = test_connection()
    if not connection:
        print("\nERROR: Cannot proceed without MySQL connection.")
        print("\nPlease ensure:")
        print("  1. MySQL/MariaDB server is running")
        print("  2. XAMPP/WAMP is started (if using)")
        print("  3. Check your .env file credentials")
        exit(1)
    
    print("\nStep 2: Creating database...")
    create_database(connection)
    
    print("\nStep 3: Setting up schema...")
    setup_schema(connection)
    
    connection.close()
    
    print("\nStep 4: Testing final connection...")
    if test_database_connection():
        print("\n" + "=" * 50)
        print("SUCCESS: Database setup complete!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("WARNING: Setup completed but connection test failed")
        print("=" * 50)
