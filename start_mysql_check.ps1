# Quick MySQL Check and Start Script for Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Quick Poll App - MySQL Setup Helper" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check for XAMPP
$xamppPath = "C:\xampp\mysql\bin\mysqld.exe"
$wampPath = "C:\wamp64\bin\mysql\mysql*\bin\mysqld.exe"

if (Test-Path $xamppPath) {
    Write-Host "[FOUND] XAMPP MySQL detected" -ForegroundColor Green
    Write-Host "To start MySQL:" -ForegroundColor Yellow
    Write-Host "1. Open XAMPP Control Panel" -ForegroundColor Yellow
    Write-Host "2. Click 'Start' next to MySQL" -ForegroundColor Yellow
    Write-Host "3. Then run: python backend\setup_database.py" -ForegroundColor Yellow
} elseif (Test-Path (Resolve-Path $wampPath -ErrorAction SilentlyContinue)) {
    Write-Host "[FOUND] WAMP MySQL detected" -ForegroundColor Green
    Write-Host "Make sure MySQL is running in WAMP" -ForegroundColor Yellow
} else {
    Write-Host "[NOT FOUND] MySQL installation not detected" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install one of the following:" -ForegroundColor Yellow
    Write-Host "1. XAMPP: https://www.apachefriends.org/ (includes MySQL/MariaDB)" -ForegroundColor Yellow
    Write-Host "2. MySQL: https://dev.mysql.com/downloads/installer/" -ForegroundColor Yellow
    Write-Host "3. MariaDB: https://mariadb.org/download/" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Checking if MySQL is running on port 3306..." -ForegroundColor Cyan
$port3306 = netstat -ano | findstr ":3306"
if ($port3306) {
    Write-Host "[OK] MySQL appears to be running on port 3306" -ForegroundColor Green
    Write-Host "You can now run: python backend\setup_database.py" -ForegroundColor Green
} else {
    Write-Host "[NOT RUNNING] MySQL is not running on port 3306" -ForegroundColor Red
    Write-Host "Please start MySQL service first" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to continue"

