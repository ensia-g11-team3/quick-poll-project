# Quick Guide: Starting MySQL for Quick Poll App

## Current Status: MySQL is NOT running ❌

Port 3306 is not active, which means MySQL server needs to be started.

---

## 🔧 How to Start MySQL

### Method 1: XAMPP (Most Common)

1. **Find XAMPP Control Panel:**
   - Look for XAMPP in Start Menu
   - Or navigate to: `C:\xampp\xampp-control.exe`

2. **Start MySQL:**
   - Open XAMPP Control Panel
   - Find "MySQL" in the list
   - Click the **"Start"** button
   - Wait until status changes to **"Running"** (green)

3. **Verify:**
   ```powershell
   netstat -ano | findstr ":3306"
   ```
   You should see output if MySQL is running.

---

### Method 2: WAMP Server

1. **Right-click WAMP icon** in system tray (bottom-right)
2. Ensure MySQL shows as **"Running"** (green icon)
3. If not running, click **"Start All Services"**

---

### Method 3: Windows Services (If MySQL installed as service)

1. Press `Win + R`
2. Type: `services.msc` and press Enter
3. Find service named:
   - "MySQL" or
   - "MySQL80" or
   - "MySQL57" or
   - "MariaDB"
4. **Right-click** → **Start**

**Or via PowerShell (Run as Administrator):**
```powershell
Start-Service MySQL
# or
Start-Service MySQL80
```

---

### Method 4: Command Line (If MySQL is in PATH)

Open PowerShell/CMD as **Administrator**:
```powershell
net start MySQL
# or
net start MySQL80
```

---

## ✅ After Starting MySQL

Once MySQL is running, run the database setup:

```powershell
cd backend
.\venv\bin\python.exe setup_database.py
```

**Or use the helper script:**
```powershell
cd backend
.\quick_start_database.bat
```

---

## 🔍 Verify MySQL is Running

After starting, verify with:
```powershell
netstat -ano | findstr ":3306"
```

**Expected output if running:**
```
TCP    0.0.0.0:3306           0.0.0.0:0              LISTENING       [PID]
```

---

## ❓ Don't Have MySQL Installed?

If you don't have MySQL installed, you have these options:

### Option A: Install XAMPP (Recommended - Easy)
1. Download from: https://www.apachefriends.org/
2. Install XAMPP (includes MySQL/MariaDB)
3. Start MySQL from XAMPP Control Panel

### Option B: Install MySQL Standalone
1. Download MySQL Community Server: https://dev.mysql.com/downloads/mysql/
2. Install and configure
3. Start the MySQL service

---

## 📝 Database Configuration

After starting MySQL, the app will connect using these settings (from `backend/.env`):
- **Host:** localhost
- **Port:** 3306
- **User:** root
- **Password:** (empty by default)
- **Database:** quick_poll_db (will be created automatically)

If your MySQL has a password, edit `backend/.env`:
```
DB_PASSWORD=your_password_here
```

---

## 🚀 Next Steps

1. ✅ Start MySQL (choose one method above)
2. ✅ Verify it's running: `netstat -ano | findstr ":3306"`
3. ✅ Run setup script: `backend\quick_start_database.bat`
4. ✅ Your app will automatically connect!

---

**Need help?** Check which method works for your setup and let me know!

