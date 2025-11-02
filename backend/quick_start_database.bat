@echo off
echo ============================================
echo Quick Poll App - Database Setup Helper
echo ============================================
echo.

REM Check if MySQL is running
netstat -ano | findstr ":3306" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] MySQL is already running on port 3306
    echo.
    echo Running database setup...
    call venv\bin\python.exe setup_database.py
    pause
    exit /b 0
)

echo [WARNING] MySQL is NOT running on port 3306
echo.
echo Please start MySQL using one of these methods:
echo.
echo 1. XAMPP Control Panel:
echo    - Open XAMPP Control Panel
echo    - Click "Start" next to MySQL
echo.
echo 2. WAMP Server:
echo    - Right-click WAMP icon in system tray
echo    - Ensure MySQL is running (green icon)
echo.
echo 3. Windows Services:
echo    - Press Win+R, type: services.msc
echo    - Find "MySQL" service and start it
echo.
echo 4. Command Line (as Administrator):
echo    - Run: net start MySQL
echo.
echo After starting MySQL, run this script again or:
echo   python setup_database.py
echo.
pause

