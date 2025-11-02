# How to Start MySQL Database

The application needs MySQL/MariaDB to be running. Follow these steps:

## Option 1: Using XAMPP (Recommended if installed)

1. Open XAMPP Control Panel
2. Click "Start" next to MySQL
3. Wait until MySQL status shows as "Running"

## Option 2: Using WAMP (If installed)

1. Open WAMP Server
2. Click on the WAMP icon in system tray
3. Make sure MySQL service is green (running)

## Option 3: Using MySQL Service

If you have MySQL installed as a Windows service:

1. Open Services (Win + R, type `services.msc`)
2. Find "MySQL" or "MySQL80" service
3. Right-click and select "Start"

## Option 4: Command Line (if MySQL is in PATH)

Open Command Prompt or PowerShell as Administrator and run:
```bash
net start MySQL
```

## After Starting MySQL

Once MySQL is running, run the setup script:
```bash
cd backend
.\venv\bin\python.exe setup_database.py
```

Or if using the main Python:
```bash
cd backend
python setup_database.py
```

## Verify MySQL is Running

Check if MySQL is listening on port 3306:
```powershell
netstat -ano | findstr ":3306"
```

You should see output like:
```
TCP    0.0.0.0:3306           0.0.0.0:0              LISTENING       [PID]
```

## Troubleshooting

If you get connection errors:
1. Make sure MySQL service is actually running
2. Check the port in your `.env` file (default is 3306)
3. Verify your MySQL username and password in `backend/.env`
4. Try connecting with phpMyAdmin (usually at http://localhost/phpmyadmin)

## Default Credentials

The `.env` file uses these defaults:
- Host: localhost
- Port: 3306
- User: root
- Password: (empty)

If your MySQL has a different password, update the `DB_PASSWORD` in `backend/.env`

