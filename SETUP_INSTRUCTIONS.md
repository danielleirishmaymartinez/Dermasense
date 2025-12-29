# DermaSense Complete Setup Instructions

## 🎯 System Overview

DermaSense is a fully functional web-based IT system for skin lesion risk assessment with:
- PostgreSQL database for data persistence
- User authentication (JWT-based)
- Machine learning model integration
- Complete frontend and backend

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Node.js 16+** and npm installed
3. **PostgreSQL** installed and running
4. **Trained ML models** (optional - system works in placeholder mode)

## 🗄️ Step 1: Database Setup

### 1.1 Install PostgreSQL

**Windows:**
- Download from https://www.postgresql.org/download/windows/
- Install with default settings
- Remember the postgres user password

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 1.2 Create Database

Open terminal/command prompt and run:

```bash
psql -U postgres
```

Then in psql:

```sql
CREATE DATABASE dermasense;
\q
```

### 1.3 Configure Environment

1. Navigate to `backend` folder
2. Create `.env` file (copy from `.env.example` if exists):
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/dermasense
   SECRET_KEY=your-secret-key-here
   ```

3. Generate a secure SECRET_KEY:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   Copy the output to SECRET_KEY in `.env`

## 🔧 Step 2: Backend Setup

### 2.1 Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2.2 Verify Database Connection

The database tables will be created automatically when you start the server.

### 2.3 Start Backend Server

```bash
python main.py
```

You should see:
```
✓ Models loaded successfully. Classes: [...]
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Note:** If models are not loaded, the system will run in placeholder mode.

## 🎨 Step 3: Frontend Setup

### 3.1 Install Dependencies

```bash
cd frontend
npm install
```

### 3.2 Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🚀 Step 4: First Run

1. **Open browser:** Navigate to `http://localhost:5173`

2. **Register an account:**
   - Click "Get Started" or go to `/register`
   - Fill in email, username, password
   - Click "Create Account"

3. **Login:**
   - After registration, you'll be auto-logged in
   - Or go to `/login` to sign in

4. **Create first assessment:**
   - Go to Dashboard
   - Click "New Risk Assessment"
   - Upload a skin lesion image
   - Fill optional inputs
   - Get risk assessment result

## 📁 Project Structure

```
Dermasense/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── auth.py              # Authentication logic
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables
│   ├── models/              # ML model files
│   └── uploads/             # User uploaded images
│
├── frontend/
│   ├── src/
│   │   ├── views/           # Page components
│   │   ├── components/      # Reusable components
│   │   ├── router/          # Vue Router config
│   │   └── api/             # API client
│   └── package.json         # Node dependencies
│
└── DATABASE_SETUP_GUIDE.md  # Detailed DB guide
```

## 🔐 Authentication Flow

1. **Registration:** User creates account → stored in `users` table
2. **Login:** User authenticates → receives JWT token
3. **Protected Routes:** Token sent with each request
4. **Token Expiry:** 30 days (configurable)

## 🗃️ Database Schema

### Users Table
- Stores user accounts
- Hashed passwords (bcrypt)
- UUID for each user

### Assessments Table
- Links to user via `user_id`
- Stores risk assessment results
- Stores uploaded image paths
- JSON fields for explanations and user inputs

## 🧪 Testing the System

### Test Registration:
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123",
    "full_name": "Test User"
  }'
```

### Test Login:
```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

## 🐛 Troubleshooting

### Database Connection Error
- Check PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in `.env`
- Check firewall (port 5432)

### Models Not Loading
- System works in placeholder mode
- Place trained models in `backend/models/`:
  - `cnn_densenet201_feature_extractor.h5`
  - `rf_densenet201_bcc_scc.pkl`
  - `class_names.npy`

### Frontend Can't Connect to Backend
- Ensure backend is running on port 8000
- Check CORS settings in `main.py`
- Verify API base URL in `frontend/src/api/client.js`

### Authentication Issues
- Check token in localStorage (browser DevTools)
- Verify SECRET_KEY in `.env`
- Check token expiry (30 days default)

## 📝 Important Notes

1. **SECRET_KEY:** Change the default SECRET_KEY in production!
2. **Database Password:** Use strong passwords in production
3. **HTTPS:** Use HTTPS in production for security
4. **Backups:** Set up regular database backups
5. **Environment:** Use different `.env` files for dev/prod

## 🎓 For Thesis Presentation

The system is now complete with:
- ✅ User authentication and registration
- ✅ PostgreSQL database integration
- ✅ User profile management
- ✅ Risk assessment with ML models
- ✅ Assessment history and monitoring
- ✅ Report generation
- ✅ Educational resources
- ✅ Professional UI/UX

**Ready for thesis demonstration!**

## 📞 Next Steps

1. Insert your trained ML models when ready
2. Test all features thoroughly
3. Prepare demo data
4. Document any customizations
5. Prepare presentation materials

---

**System Status:** ✅ Fully Functional (except ML models - use placeholder mode)

