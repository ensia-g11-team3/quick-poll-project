# Quick Poll App - Quick Reference

Fast reference guide for running and using the Quick Poll App.

## 🚀 Quick Start (2 Minutes)

### 1. Start Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
python app.py
```
✅ Backend running at `http://localhost:5000`

### 2. Start Frontend
```bash
cd frontend
npm install
npm start
```
✅ Frontend opens at `http://localhost:3000`

## 📚 Documentation Files

| File | Description |
|------|-------------|
| [README.md](README.md) | Main project documentation |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Detailed setup instructions |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete API reference |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | This file - quick commands |
| [backend/README.md](backend/README.md) | Backend-specific docs |
| [frontend/README.md](frontend/README.md) | Frontend-specific docs |

## 🎯 Common Commands

### Backend
```bash
# Activate venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac

# Run server
python app.py

# Install dependencies
pip install -r requirements.txt
```

### Frontend
```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## 🔍 Testing Endpoints

### Browser
- Get all polls: `http://localhost:5000/api/polls`
- Backend health: `http://localhost:5000/api/polls`

### cURL
```bash
# Create poll
curl -X POST http://localhost:5000/api/polls \
  -H "Content-Type: application/json" \
  -d '{"question": "Test?", "options": ["Yes", "No"]}'

# Get poll (replace LINK with actual link)
curl http://localhost:5000/api/polls/LINK
```

## 🗄️ Database

- **Location**: `backend/quick_poll_db.sqlite`
- **Type**: SQLite (auto-created)
- **Reset**: Delete the `.sqlite` file

## 🌐 URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **API Docs**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5000 in use | `netstat -ano \| findstr :5000` then `taskkill /PID <PID> /F` |
| Port 3000 in use | React will prompt for another port |
| Module not found | Activate venv and run `pip install -r requirements.txt` |
| npm errors | `rm -rf node_modules && npm install` |
| Database errors | Delete `backend/quick_poll_db.sqlite` |

## 📋 Project Structure Quick View

```
PROJECT SE/
├── frontend/          # React app (port 3000)
├── backend/           # Flask API (port 5000)
├── database/          # SQL schema (reference)
└── *.md              # Documentation
```

## 🎨 Features Checklist

- [x] Create polls with questions
- [x] Add dynamic options (min 2)
- [x] Vote on polls
- [x] View results
- [x] Share via unique links
- [x] Real-time vote counts
- [x] Responsive design
- [x] Form validation

## 📞 Need Help?

1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup
2. See [README.md](README.md) for full documentation
3. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
4. Check browser console (F12) for frontend errors
5. Check backend terminal for API errors

---

**Happy Polling! 🎉**

