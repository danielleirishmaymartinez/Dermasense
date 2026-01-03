# DermaSense - Complete System with Database & Authentication

## ✅ System Overview

Your DermaSense system now includes:

1. **PostgreSQL Database Integration**
   - User accounts and authentication
   - Assessment history storage
   - Image storage in database (binary data)
   
2. **User Authentication System**
   - User registration
   - User login with JWT tokens
   - Protected routes requiring authentication
   - User profile management

3. **Complete Frontend Integration**
   - Login page
   - Registration page
   - User profile page
   - Protected routes with authentication guards
   - Dynamic navbar with login/logout

## 📋 Setup Instructions

### Step 1: Database Setup

Follow the detailed instructions in `DATABASE_SETUP_GUIDE.md` to:
1. Install PostgreSQL (if not already installed)
2. Create database and user
3. Configure environment variables

### Step 2: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Configure Environment

1. Copy the example environment file:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. Edit `.env` file with your database credentials:
   ```
   DATABASE_URL=postgresql://dermasense_user:dermasense_password@localhost:5432/dermasense_db
   SECRET_KEY=your-secret-key-here
   ```

3. Generate a secure SECRET_KEY:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

### Step 4: Start Backend Server

```bash
cd backend
python main.py
```

The database tables will be automatically created on first startup.

### Step 5: Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Step 6: Start Frontend Server

```bash
cd frontend
npm run dev
```

## 🚀 Usage Flow

1. **First Time User:**
   - Visit http://localhost:5173
   - Click "Sign Up" or navigate to `/register`
   - Create an account with email, username, and password
   - You'll be automatically logged in after registration

2. **Existing User:**
   - Visit http://localhost:5173
   - Click "Login" or navigate to `/login`
   - Enter username/email and password

3. **After Login:**
   - Access Dashboard to see your assessments
   - Upload images for risk assessment (requires authentication)
   - View monitoring history
   - Access your profile page

## 📁 Database Schema

### Users Table
- `id` (UUID) - Primary key
- `email` (String) - Unique user email
- `username` (String) - Unique username
- `hashed_password` (String) - Bcrypt hashed password
- `full_name` (String, optional) - User's full name
- `created_at` (DateTime) - Account creation timestamp
- `updated_at` (DateTime) - Last update timestamp
- `is_active` (Boolean) - Account status

### Assessments Table
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key to users
- `risk_level` (String) - LOW/MEDIUM/HIGH
- `final_risk_score` (Float) - Combined risk score
- `image_risk` (Float) - ML-based image risk
- `support_risk` (Float) - Rule-based support risk
- `explanations` (JSON) - Risk explanations
- `recommendation` (Text) - Recommendations
- `user_inputs` (JSON) - User-provided information
- `created_at` (DateTime) - Assessment timestamp

### Images Table
- `id` (UUID) - Primary key
- `assessment_id` (UUID) - Foreign key to assessments
- `user_id` (UUID) - Foreign key to users
- `image_data` (BYTEA) - Binary image data
- `filename` (String) - Original filename
- `content_type` (String) - MIME type (e.g., "image/jpeg")
- `file_size` (Integer) - File size in bytes
- `created_at` (DateTime) - Upload timestamp

## 🔐 Authentication

- **Token Type:** JWT (JSON Web Token)
- **Token Expiry:** 30 days
- **Password Hashing:** Bcrypt
- **Token Storage:** localStorage (frontend)

## 🔌 API Endpoints

### Authentication Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user (returns JWT token)
- `GET /auth/me` - Get current user info
- `GET /users/profile` - Get user profile with statistics

### Assessment Endpoints (Require Authentication)
- `POST /assess-risk` - Upload image and get risk assessment
- `GET /assessments` - Get user's assessment history
- `GET /assessments/{id}` - Get specific assessment
- `GET /assessments/{id}/image` - Get assessment image
- `DELETE /assessments/{id}` - Delete assessment

### Public Endpoints
- `GET /` - API information

## 🛡️ Protected Routes

The following frontend routes require authentication:
- `/dashboard`
- `/upload`
- `/analyzing`
- `/results`
- `/monitoring`
- `/reports`
- `/profile`

If a user tries to access these routes without being logged in, they'll be redirected to the login page.

## 📝 Notes

1. **Database Connection:** Make sure PostgreSQL is running before starting the backend
2. **Environment Variables:** Never commit `.env` file to version control
3. **SECRET_KEY:** Always use a strong, random SECRET_KEY in production
4. **Password Security:** Passwords are hashed using bcrypt before storage
5. **Image Storage:** Images are stored as binary data (BYTEA) in PostgreSQL

## 🐛 Troubleshooting

### Database Connection Errors
- Verify PostgreSQL is running
- Check DATABASE_URL in `.env` file
- Ensure database and user exist (see DATABASE_SETUP_GUIDE.md)

### Authentication Issues
- Clear browser localStorage and try logging in again
- Check backend logs for token validation errors
- Verify SECRET_KEY is set in `.env` file

### Tables Not Created
- Check backend startup logs for errors
- Manually run: `python -c "from database import init_db; init_db()"`

## 🎓 For Thesis Documentation

The system now includes:
- ✅ Complete database integration (PostgreSQL)
- ✅ User authentication and authorization
- ✅ User registration and login
- ✅ Protected API endpoints
- ✅ User profile management
- ✅ Image storage in database
- ✅ Assessment history tracking
- ✅ Complete frontend authentication flow
- ✅ Production-ready security practices

**System Status:** ✅ Fully Functional and Ready for Thesis Presentation

---

For detailed database setup instructions, see `DATABASE_SETUP_GUIDE.md`

