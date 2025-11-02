# Database Setup Guide

## Quick Poll App - MySQL/MariaDB Setup

### Option 1: Using XAMPP (Recommended for Windows)

1. **Download and Install XAMPP** (if not already installed):
   - Download from: https://www.apachefriends.org/
   - Install XAMPP which includes MySQL/MariaDB

2. **Start MySQL in XAMPP**:
   - Open XAMPP Control Panel
   - Click "Start" next to MySQL
   - MySQL should start on port 3306

3. **Access phpMyAdmin**:
   - Click "Admin" next to MySQL in XAMPP Control Panel
   - Or go to: http://localhost/phpmyadmin

4. **Create Database**:
   - Click "New" in the left sidebar
   - Database name: `quick_poll_db`
   - Collation: `utf8mb4_general_ci`
   - Click "Create"

5. **Import Schema**:
   - Select the `quick_poll_db` database
   - Click "Import" tab
   - Choose file: `database/schema.sql`
   - Click "Go"

### Option 2: Using Standalone MySQL/MariaDB

1. **Start MySQL Service**:
   ```powershell
   # Check if MySQL service exists
   Get-Service | Where-Object {$_.Name -like "*mysql*"}
   
   # Start MySQL service (replace service name)
   Start-Service MySQL80
   # or
   Start-Service MariaDB
   ```

2. **Run Setup Script**:
   ```bash
   cd backend
   python setup_database.py
   ```

### Option 3: Manual Setup via Command Line

1. **Connect to MySQL**:
   ```bash
   mysql -u root -p
   ```

2. **Create Database**:
   ```sql
   CREATE DATABASE quick_poll_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
   USE quick_poll_db;
   ```

3. **Import Schema**:
   ```bash
   mysql -u root -p quick_poll_db < database/schema.sql
   ```

### Configure Database Connection

Update `backend/.env` file with your database credentials:

```env
DB_HOST=localhost
DB_NAME=quick_poll_db
DB_USER=root
DB_PASSWORD=your_password_here
DB_PORT=3306
```

**Note**: If using XAMPP with default settings, leave `DB_PASSWORD` empty:
```env
DB_PASSWORD=
```

### Verify Setup

After setting up, run the setup script to verify:

```bash
cd backend
python setup_database.py
```

Or test the connection manually:

```bash
mysql -u root -p -e "USE quick_poll_db; SHOW TABLES;"
```

You should see 4 tables:
- `users`
- `polls`
- `options`
- `votes`

### Troubleshooting

**Error: Can't connect to MySQL server**
- Make sure MySQL/MariaDB service is running
- Check if port 3306 is being used: `netstat -ano | findstr :3306`
- Verify credentials in `.env` file

**Error: Access denied**
- Check username and password in `.env` file
- For XAMPP, default user is `root` with no password
- Try resetting MySQL root password if needed

**Error: Database already exists**
- This is fine, the setup script will use existing database
- Tables will be created if they don't exist

