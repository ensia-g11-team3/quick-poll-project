# Quick Poll App - Setup Guide

A step-by-step guide to get the Quick Poll App up and running on your machine.

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Node.js 16+** installed ([Download](https://nodejs.org/))
- [ ] **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- [ ] **Git** (optional) installed
- [ ] Text editor or IDE (VS Code recommended)

### Verify Installations

**Check Node.js:**
```bash
node --version
npm --version
```

**Check Python:**
```bash
python --version
# or
python3 --version
pip --version
```

## 🚀 Installation Steps

### Step 1: Get the Project

**Option A: Clone Repository (if using Git)**
```bash
git clone <repository-url>
cd "PROJECT SE"
```

**Option B: Extract Downloaded Folder**
- Extract the project folder to your desired location
- Navigate to the project folder

### Step 2: Backend Setup

1. **Open Terminal/PowerShell** in the project root

2. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

3. **Create Virtual Environment:**
   
   **Windows:**
   ```powershell
   python -m venv venv
   ```
   
   **Linux/Mac:**
   ```bash
   python3 -m venv venv
   ```

4. **Activate Virtual Environment:**
   
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
   
   You should see `(venv)` at the start of your terminal prompt.

5. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This installs:
   - Flask
   - Flask-CORS
   - Flask-Bcrypt (optional)
   - python-dotenv

6. **Verify Installation:**
   ```bash
   python app.py
   ```
   
   You should see:
   ```
   ==================================================
   Quick Poll App - Backend Server
   ==================================================
   Database: C:\...\backend\quick_poll_db.sqlite
   Starting server on http://localhost:5000
   ==================================================
   * Running on http://127.0.0.1:5000
   ```
   
   Press `Ctrl+C` to stop the server.

### Step 3: Frontend Setup

1. **Open a NEW Terminal/PowerShell** window

2. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

3. **Install Dependencies:**
   ```bash
   npm install
   ```
   
   This may take a few minutes. It installs:
   - React
   - React Router
   - Axios
   - React Scripts

4. **Verify Installation:**
   ```bash
   npm start
   ```
   
   Your browser should open automatically to http://localhost:3000
   
   Press `Ctrl+C` to stop the server.

## ✅ Running the Application

### Method 1: Two Terminal Windows (Recommended)

**Terminal 1 - Backend Server:**
```bash
cd backend
.\venv\Scripts\Activate.ps1  # Activate venv (Windows)
# or: source venv/bin/activate  # Linux/Mac
python app.py
```

**Terminal 2 - Frontend Server:**
```bash
cd frontend
npm start
```

### Method 2: Background Processes

**Windows PowerShell:**
```powershell
# Start backend in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; .\venv\Scripts\Activate.ps1; python app.py"

# Start frontend (will open browser)
cd frontend
npm start
```

## 🎯 First Run Checklist

When running for the first time:

1. ✅ Backend starts without errors
2. ✅ Database file `quick_poll_db.sqlite` is created in `backend/` folder
3. ✅ Frontend opens in browser at http://localhost:3000
4. ✅ No console errors in browser
5. ✅ Can see "Create a New Poll" page

## 🧪 Testing the Setup

### Test 1: Backend API
Open browser and visit:
```
http://localhost:5000/api/polls
```

Should return: `{"polls": []}`

### Test 2: Create a Poll
1. Go to http://localhost:3000
2. Enter question: "What is your favorite color?"
3. Add options: "Red", "Blue", "Green"
4. Click "Create Poll"
5. Should redirect to poll page

### Test 3: Vote
1. Select an option
2. Click "Submit Vote"
3. Should show results page

## 🐛 Common Setup Issues

### Issue: Python not found
**Solution:**
- Add Python to PATH during installation
- Or use full path: `C:\Python3x\python.exe -m venv venv`

### Issue: npm not found
**Solution:**
- Reinstall Node.js
- Make sure "Add to PATH" is checked during installation

### Issue: Permission denied (venv activation)
**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Port already in use
**Solution:**
- Change port in `app.py` (backend) or `package.json` (frontend)
- Or kill the process using the port

**Windows:**
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: Module not found
**Solution:**
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Issue: npm install fails
**Solution:**
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## 📊 Project Structure Overview

```
PROJECT SE/
│
├── backend/              # Flask backend
│   ├── app.py           # Main application (run this)
│   ├── requirements.txt # Python dependencies
│   ├── venv/            # Virtual environment (created)
│   └── *.sqlite         # Database (auto-created)
│
├── frontend/            # React frontend
│   ├── src/             # Source code
│   ├── public/          # Static files
│   ├── package.json     # npm dependencies
│   └── node_modules/    # Installed packages (created)
│
└── database/            # Database schema (reference)
    └── schema.sql
```

## 🔄 Daily Development Workflow

1. **Start Backend:**
   ```bash
   cd backend
   .\venv\Scripts\Activate.ps1
   python app.py
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Make Changes:**
   - Frontend: Edit files in `frontend/src/`
   - Backend: Edit `backend/app.py`
   - Changes auto-reload (hot reload)

4. **Stop Servers:**
   - Press `Ctrl+C` in each terminal

## 📝 Next Steps

After setup:
1. ✅ Read [README.md](README.md) for features
2. ✅ Check [API Documentation](README.md#api-documentation)
3. ✅ Explore the code structure
4. ✅ Start creating polls!

## 💡 Tips

- Keep both terminals open while developing
- Check browser console (F12) for frontend errors
- Check backend terminal for API errors
- Database resets by deleting `backend/quick_poll_db.sqlite`

---

**Need Help?** Check the main [README.md](README.md) troubleshooting section!

