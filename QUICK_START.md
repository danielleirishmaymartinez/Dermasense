# DermaSense Quick Start Guide

## 🚀 Quick Setup (5 Steps)

### 1. Database Setup (PostgreSQL)

**Windows:**
```bash
# Install PostgreSQL from https://www.postgresql.org/download/windows/
# During installation, remember the postgres user password
# Then open psql and run:

psql -U postgres
CREATE DATABASE dermasense_db;
CREATE USER dermasense_user WITH PASSWORD 'dermasense_password';
GRANT ALL PRIVILEGES ON DATABASE dermasense_db TO dermasense_user;
\c dermasense_db
GRANT ALL ON SCHEMA public TO dermasense_user;
\q
```

**Linux/Mac:**
```bash
sudo -u postgres psql
# Then run the same SQL commands as above
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Create .env file
echo "DATABASE_URL=postgresql://dermasense_user:dermasense_password@localhost:5432/dermasense_db" > .env
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" >> .env

# Start backend
python main.py
```

Backend will run on: http://127.0.0.1:8000

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on: http://localhost:5173

### 4. First Use

1. Open http://localhost:5173 in your browser
2. Click "Sign Up" or go to `/register`
3. Create an account
4. You'll be automatically logged in
5. Start using the system!

### 5. Verify Database

Check that tables were created:
```bash
psql -U dermasense_user -d dermasense_db
\dt
```

You should see: `users`, `assessments`, `images`

## ✅ System Features

- ✅ User Registration & Login
- ✅ PostgreSQL Database
- ✅ Image Storage in Database
- ✅ Assessment History
- ✅ User Profile Page
- ✅ Protected Routes
- ✅ JWT Authentication

## 📚 Detailed Documentation

- **Database Setup:** See `DATABASE_SETUP_GUIDE.md`
- **Complete System Info:** See `SYSTEM_COMPLETE.md`
- **API Documentation:** Visit http://127.0.0.1:8000/docs when backend is running

## 🐛 Common Issues

**Database connection error:**
- Make sure PostgreSQL is running
- Check DATABASE_URL in `.env` file
- Verify user password is correct

**Tables not created:**
- Check backend logs for errors
- Manually create: `python -c "from database import init_db; init_db()"`

**Port already in use:**
- Backend: Change port in `main.py` or kill process using port 8000
- Frontend: Change port in `vite.config.js`

---

**Ready for Thesis!** 🎓

