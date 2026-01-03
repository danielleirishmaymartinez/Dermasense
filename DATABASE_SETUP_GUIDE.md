# PostgreSQL Database Setup Guide for DermaSense

This guide will help you set up PostgreSQL database for the DermaSense system.

## Prerequisites

1. **PostgreSQL Installation**
   - Download PostgreSQL from: https://www.postgresql.org/download/
   - Install PostgreSQL (choose a version 12 or higher)
   - During installation, remember the password you set for the `postgres` user
   - Make sure PostgreSQL service is running

## Step-by-Step Setup Instructions

### Step 1: Verify PostgreSQL Installation

Open a terminal/command prompt and verify PostgreSQL is installed:

```bash
psql --version
```

If PostgreSQL is installed, you should see the version number.

### Step 2: Access PostgreSQL

On Windows:
```bash
# Open PowerShell or Command Prompt
psql -U postgres
```

On Linux/Mac:
```bash
sudo -u postgres psql
```

You'll be prompted for the password you set during installation.

### Step 3: Create Database

Once you're in the PostgreSQL prompt (you'll see `postgres=#`), run the following commands:

```sql
-- Create database
CREATE DATABASE dermasense_db;

-- Create user
CREATE USER dermasense_user WITH PASSWORD 'dermasense_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE dermasense_db TO dermasense_user;

-- Connect to the database
\c dermasense_db

-- Grant schema privileges (PostgreSQL 15+)
GRANT ALL ON SCHEMA public TO dermasense_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dermasense_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dermasense_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dermasense_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO dermasense_user;

-- Exit PostgreSQL
\q
```

### Step 4: Verify Database Connection

Test the connection from command line:

```bash
psql -U dermasense_user -d dermasense_db -h localhost
```

Enter the password: `dermasense_password`

If successful, you'll see the prompt: `dermasense_db=>`

Type `\q` to exit.

### Step 5: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. Edit `.env` file (use any text editor):
   ```
   DATABASE_URL=postgresql://dermasense_user:dermasense_password@localhost:5432/dermasense_db
   SECRET_KEY=your-secret-key-change-this-in-production
   ```

3. Generate a secure SECRET_KEY:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   
   Copy the output and replace `your-secret-key-change-this-in-production` in `.env` file.

### Step 6: Install Python Dependencies

Make sure you have all required packages:

```bash
cd backend
pip install -r requirements.txt
```

### Step 7: Initialize Database Tables

The database tables will be automatically created when you first start the backend server. However, if you want to create them manually, you can run:

```python
from database import init_db
init_db()
```

Or simply start your backend server - it will create the tables on startup.

### Step 8: Verify Tables Created

Connect to the database and verify tables:

```bash
psql -U dermasense_user -d dermasense_db -h localhost
```

Once connected, list tables:
```sql
\dt
```

You should see three tables:
- `users`
- `assessments`
- `images`

To see table structure:
```sql
\d users
\d assessments
\d images
```

Type `\q` to exit.

## Database Schema Overview

### Users Table
- Stores user accounts and authentication information
- Fields: id, email, username, hashed_password, full_name, created_at, updated_at, is_active

### Assessments Table
- Stores risk assessment results
- Fields: id, user_id, risk_level, final_risk_score, image_risk, support_risk, explanations, recommendation, user_inputs, created_at

### Images Table
- Stores uploaded images as binary data (BYTEA)
- Fields: id, assessment_id, user_id, image_data, filename, content_type, file_size, created_at

## Troubleshooting

### Issue: "Connection refused" or "could not connect to server"

**Solution:**
1. Check if PostgreSQL service is running:
   - Windows: Services app → PostgreSQL service → Start
   - Linux: `sudo systemctl start postgresql`
   - Mac: `brew services start postgresql`

2. Verify PostgreSQL is listening on port 5432:
   ```bash
   # Windows
   netstat -an | findstr 5432
   
   # Linux/Mac
   netstat -an | grep 5432
   ```

### Issue: "password authentication failed"

**Solution:**
1. Verify the password in your `.env` file matches the database user password
2. Reset the password if needed:
   ```sql
   ALTER USER dermasense_user WITH PASSWORD 'new_password';
   ```
   Then update `.env` file accordingly.

### Issue: "permission denied for schema public"

**Solution:**
Run these commands in PostgreSQL (as postgres user):
```sql
\c dermasense_db
GRANT ALL ON SCHEMA public TO dermasense_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dermasense_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dermasense_user;
```

### Issue: Tables not created

**Solution:**
1. Check database connection string in `.env` file
2. Verify user has proper permissions
3. Check backend logs for errors
4. Manually run: `python -c "from database import init_db; init_db()"`

## Security Notes

⚠️ **Important for Production:**

1. **Change Default Passwords**: Never use default passwords in production
2. **Use Strong SECRET_KEY**: Generate a random, secure SECRET_KEY
3. **Restrict Database Access**: Only allow connections from your application server
4. **Use SSL**: Enable SSL for database connections in production
5. **Regular Backups**: Set up automated database backups
6. **Environment Variables**: Never commit `.env` file to version control

## Next Steps

After database setup:
1. Start the backend server: `python main.py`
2. The tables will be automatically created on first run
3. You can now register users and start using the system
4. Test registration and login through the frontend

## Quick Reference Commands

```bash
# Start PostgreSQL service (Windows)
net start postgresql-x64-14  # Replace with your version

# Connect to database
psql -U dermasense_user -d dermasense_db -h localhost

# List all databases
psql -U postgres -c "\l"

# List tables
psql -U dermasense_user -d dermasense_db -c "\dt"

# Backup database
pg_dump -U dermasense_user dermasense_db > backup.sql

# Restore database
psql -U dermasense_user dermasense_db < backup.sql
```

---

**Database Setup Complete!** ✅

Your DermaSense database is now ready to use. Proceed with starting the backend server.

