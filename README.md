# Quick Poll App

A full-stack web application for creating and sharing polls quickly and easily. Users can create polls with multiple options, share them via unique links, and view real-time voting results.

![Quick Poll App](https://img.shields.io/badge/Status-Ready-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18.2-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- ✅ **Create Polls**: Easy-to-use interface for creating polls with dynamic options
- ✅ **Dynamic Options**: Add/remove multiple choice options (minimum 2 required)
- ✅ **Validation**: Client and server-side validation for polls and options
- ✅ **Unique Links**: Each poll gets a unique, shareable link
- ✅ **Voting**: Simple voting interface with real-time updates
- ✅ **Results**: View poll results with vote counts and percentages
- ✅ **Responsive Design**: Beautiful, modern UI that works on all devices
- ✅ **Real-time Updates**: Poll results update automatically
- ✅ **Anonymous Voting**: Users can vote without registration
- ✅ **User Authentication**: Optional user registration/login (when bcrypt is available)

## 🛠 Tech Stack

### Frontend
- **React.js 18.2** - Modern UI library
- **React Router** - Client-side routing
- **Axios** - HTTP client for API requests
- **CSS3** - Modern styling with gradients and animations

### Backend
- **Python 3.8+** - Programming language
- **Flask 3.0** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite3** - Lightweight database (built into Python)

### Database
- **SQLite** - File-based database (no installation required)

## 📁 Project Structure

```
PROJECT SE/
├── frontend/                 # React frontend application
│   ├── public/              # Static files
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── CreatePoll.js    # Poll creation form
│   │   │   ├── PollView.js      # Poll voting interface
│   │   │   └── PollResults.js   # Results display
│   │   ├── services/        # API service layer
│   │   │   └── api.js       # API client functions
│   │   ├── App.js           # Main app component
│   │   └── index.js         # Entry point
│   ├── package.json         # Dependencies
│   └── README.md
│
├── backend/                  # Flask backend API
│   ├── app.py               # Main Flask application
│   ├── requirements.txt     # Python dependencies
│   ├── quick_poll_db.sqlite # SQLite database (auto-created)
│   └── README.md
│
├── database/                 # Database schema
│   └── schema.sql           # MySQL schema (for reference)
│
└── README.md                # This file
```

## 🚀 Installation

### Prerequisites

- **Node.js 16+** and npm (for frontend)
- **Python 3.8+** and pip (for backend)
- **Git** (optional, for cloning)

### Step 1: Clone or Download

If using Git:
```bash
git clone <repository-url>
cd "PROJECT SE"
```

Or download and extract the project folder.

### Step 2: Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:

   **Windows (PowerShell):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   **Windows (CMD):**
   ```cmd
   venv\Scripts\activate
   ```

   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

The required packages are:
- Flask==3.0.0
- Flask-CORS==4.0.0
- Flask-Bcrypt==1.0.1 (optional, for user authentication)
- python-dotenv==1.0.0

### Step 3: Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install npm dependencies:
```bash
npm install
```

This will install:
- React 18.2.0
- React Router DOM 6.20.0
- Axios 1.6.2
- React Scripts 5.0.1

## 🏃 Quick Start

### Running the Application

You need to run both the backend and frontend servers.

#### Option 1: Run Both Servers (Recommended)

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```
Backend will start on `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```
Frontend will start on `http://localhost:3000` and open automatically in your browser.

#### Option 2: Using Helper Scripts (Windows)

**Backend:**
```powershell
cd backend
.\venv\bin\python.exe app.py
```

**Frontend:**
```powershell
cd frontend
npm start
```

### First Run

On first run:
1. The backend will automatically create the SQLite database file (`quick_poll_db.sqlite`)
2. All required tables will be created automatically
3. No database configuration needed!

### Access the Application

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:5000/api

## 📖 Usage Guide

### Creating a Poll

1. Open http://localhost:3000
2. Enter your poll question (max 200 characters)
3. Add at least 2 options (use "+ Add Choice" to add more)
4. Click "Create Poll"
5. You'll be redirected to the poll page with a shareable link

### Voting on a Poll

1. Open a poll link (e.g., `http://localhost:3000/poll/abc123`)
2. Select your preferred option
3. Click "Submit Vote"
4. View results immediately

### Viewing Results

1. On any poll page, click "View Results"
2. See vote counts and percentages
3. Results update in real-time

### Sharing Polls

Each poll has a unique link:
- Copy the link from the poll page
- Share via email, social media, or messaging apps
- Anyone with the link can vote

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### Polls

**Create Poll**
```
POST /api/polls
Content-Type: application/json

{
  "question": "What is your favorite color?",
  "options": ["Red", "Blue", "Green"],
  "creator_id": null  // Optional
}

Response: {
  "message": "Poll created successfully",
  "poll_id": 1,
  "poll_link": "abc123xyz"
}
```

**Get Poll**
```
GET /api/polls/{poll_link}

Response: {
  "poll": {
    "poll_id": 1,
    "question": "What is your favorite color?",
    "poll_link": "abc123xyz",
    "created_at": "2025-11-01T12:00:00",
    "options": [
      {
        "option_id": 1,
        "option_text": "Red",
        "vote_count": 5
      },
      ...
    ]
  }
}
```

**Get All Polls**
```
GET /api/polls

Response: {
  "polls": [...]
}
```

**Get Poll Results**
```
GET /api/polls/{poll_link}/results

Response: {
  "poll": {
    "poll_id": 1,
    "question": "What is your favorite color?",
    "total_votes": 10,
    "options": [
      {
        "option_id": 1,
        "option_text": "Red",
        "vote_count": 5,
        "percentage": 50.0
      },
      ...
    ]
  }
}
```

#### Votes

**Submit Vote**
```
POST /api/votes
Content-Type: application/json

{
  "poll_id": 1,
  "option_id": 1,
  "voter_id": null  // Optional, null for anonymous
}

Response: {
  "message": "Vote submitted successfully",
  "vote_id": 1
}
```

#### Users (Optional - requires bcrypt)

**Register User**
```
POST /api/users/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Login User**
```
POST /api/users/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}
```

## 🛠 Development

### Project Architecture

```
┌─────────────┐         HTTP/REST          ┌─────────────┐
│   React     │ ◄────────────────────────► │   Flask     │
│  Frontend   │                             │   Backend   │
│ (Port 3000) │                             │ (Port 5000) │
└─────────────┘                             └──────┬──────┘
                                                   │
                                                   │ SQLite
                                                   ▼
                                            ┌─────────────┐
                                            │   Database  │
                                            │ (SQLite)    │
                                            └─────────────┘
```

### Database Schema

The application uses the following tables:

- **users**: User accounts (optional)
- **polls**: Poll information
- **options**: Poll choice options
- **votes**: Vote records

See `database/schema.sql` for detailed schema structure.

### Environment Variables

Optional `.env` file in `backend/` directory:
```
DB_HOST=localhost
DB_NAME=quick_poll_db
DB_USER=root
DB_PASSWORD=
DB_PORT=3306
```

**Note:** Currently using SQLite, so these are not required. They're kept for future MySQL support.

### Adding Features

1. **Frontend**: Add components in `frontend/src/components/`
2. **Backend**: Add routes in `backend/app.py`
3. **API**: Add service functions in `frontend/src/services/api.js`

## 🔧 Troubleshooting

### Backend Issues

**Problem: Port 5000 already in use**
```bash
# Windows: Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in app.py:
app.run(debug=True, port=5001)
```

**Problem: Module not found**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: Database connection error**
- SQLite database is created automatically
- Check file permissions in `backend/` directory
- Delete `quick_poll_db.sqlite` to reset database

### Frontend Issues

**Problem: Port 3000 already in use**
```bash
# React will ask to use a different port
# Or kill the process:
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Problem: npm install fails**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

**Problem: API connection error**
- Ensure backend is running on port 5000
- Check CORS settings in `backend/app.py`
- Verify API URL in `frontend/src/services/api.js`

### General Issues

**Problem: Both servers not starting**
- Check if ports 3000 and 5000 are available
- Ensure Node.js and Python are installed
- Verify all dependencies are installed

**Problem: Polls not saving**
- Check browser console for errors
- Verify backend is running
- Check database file exists in `backend/`

## 📝 Notes

- **SQLite Database**: The database file (`quick_poll_db.sqlite`) is created automatically in the `backend/` directory
- **No MySQL Required**: The app uses SQLite by default (no installation needed)
- **User Authentication**: Optional feature, requires bcrypt installation
- **Data Persistence**: All data is stored locally in the SQLite file
- **Development Mode**: Both servers run in debug mode for development

## 🎯 Future Enhancements

- [ ] User authentication with sessions
- [ ] Poll expiration dates
- [ ] Multiple choice voting
- [ ] Poll analytics dashboard
- [ ] Email notifications
- [ ] Export poll results
- [ ] Mobile app version

## 📄 License

This project is part of a software engineering course.

## 👥 Contributors

- Project Team

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the API documentation
3. Check server logs for error messages

---

**Happy Polling! 🎉**
