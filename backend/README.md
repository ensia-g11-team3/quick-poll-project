# Quick Poll App - Backend

Flask RESTful API backend for the Quick Poll App.

## 📋 Overview

The backend provides a RESTful API for poll creation, voting, and result retrieval. It uses Flask with SQLite for data persistence.

## 🚀 Quick Start

### Installation

1. **Create virtual environment:**
```bash
python -m venv venv
```

2. **Activate virtual environment:**

   **Windows:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the server:**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## 📁 Project Structure

```
backend/
├── app.py                   # Main Flask application
├── requirements.txt         # Python dependencies
├── quick_poll_db.sqlite    # SQLite database (auto-created)
├── .env                     # Environment variables (optional)
└── README.md               # This file
```

## 🗄️ Database

### SQLite (Default)

The app uses SQLite by default - **no installation required!**

- Database file: `quick_poll_db.sqlite` (auto-created on first run)
- Tables are automatically initialized
- Located in the `backend/` directory

### Database Schema

The application automatically creates these tables:

- **users**: User accounts (optional)
- **polls**: Poll information
- **options**: Poll choice options
- **votes**: Vote records

See `database/schema.sql` for detailed schema.

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in the backend directory:

```bash
DB_HOST=localhost
DB_NAME=quick_poll_db
DB_USER=root
DB_PASSWORD=
DB_PORT=3306
```

**Note:** Currently using SQLite, so these are not required. They're kept for future MySQL support.

## 📡 API Endpoints

### Polls
- `POST /api/polls` - Create a new poll with options
- `GET /api/polls/<poll_link>` - Get poll details
- `GET /api/polls` - Get all polls
- `GET /api/polls/<poll_link>/results` - Get poll results with vote counts

### Votes
- `POST /api/votes` - Submit a vote

### Users (Optional - requires bcrypt)
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login user

For complete API documentation, see [API_DOCUMENTATION.md](../API_DOCUMENTATION.md)

## 🛠 Technologies

- **Flask 3.0.0** - Web framework
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **SQLite3** - Database (built into Python)
- **Flask-Bcrypt 1.0.1** - Password hashing (optional)

## 🔒 Security Features

- Password hashing (when bcrypt available)
- SQL injection prevention (parameterized queries)
- Input validation
- CORS enabled for frontend communication

## 🧪 Testing

### Manual Testing

Test the API using cURL or browser:

```bash
# Get all polls
curl http://localhost:5000/api/polls

# Create a poll
curl -X POST http://localhost:5000/api/polls \
  -H "Content-Type: application/json" \
  -d '{"question": "Test?", "options": ["Yes", "No"]}'
```

### Health Check

Visit `http://localhost:5000/api/polls` in your browser - should return `{"polls": []}`

## 🐛 Troubleshooting

### Port 5000 already in use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in app.py:
app.run(debug=True, port=5001)
```

### Module not found
- Make sure virtual environment is activated
- Reinstall: `pip install -r requirements.txt`

### Database errors
- Delete `quick_poll_db.sqlite` to reset database
- Check file permissions in `backend/` directory

### Import errors
- Verify all dependencies are installed
- Check Python version (requires 3.8+)

## 📝 Development Notes

- **Debug Mode**: Enabled by default for development
- **Auto-reload**: Code changes reload automatically
- **Database**: SQLite file is created automatically
- **CORS**: Enabled for all origins (configure for production)

## 🔄 Adding New Endpoints

1. Add route decorator in `app.py`:
```python
@app.route('/api/endpoint', methods=['GET', 'POST'])
def endpoint():
    # Implementation
    return jsonify({'data': 'value'})
```

2. Update frontend API service if needed
3. Test with cURL or Postman

## 📊 Database Management

### Reset Database
Delete `quick_poll_db.sqlite` file - it will be recreated on next run.

### Backup Database
Simply copy `quick_poll_db.sqlite` to backup location.

### View Database (Optional)
Use SQLite browser tools:
- DB Browser for SQLite
- SQLiteStudio
- VS Code SQLite extension

## 🚀 Production Deployment

For production:
1. Set `debug=False` in `app.py`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure proper CORS settings
4. Set up proper database (consider PostgreSQL/MySQL)
5. Use environment variables for sensitive data
6. Enable HTTPS

For more information, see the main [README.md](../README.md)

