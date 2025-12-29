# DermaSense: Machine Learning–Assisted Skin Lesion Risk Assessment System

A fully functional web-based system for skin lesion risk assessment using deep learning and rule-based scoring.

## 🎯 System Overview

DermaSense is a **risk assessment tool** (NOT a diagnostic tool) that:
- Analyzes skin lesion images using DenseNet201 + Random Forest
- Combines ML predictions with rule-based user inputs
- Provides Low/Medium/High risk levels with explanations
- Supports long-term monitoring and reporting

## ⚠️ Important Disclaimer

> **This system is for risk assessment only and not a medical diagnosis. Always consult a dermatologist for professional evaluation.**

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, for user authentication)
- Your trained ML models in `backend/models/`:
  - `risk_cnn_densenet201.h5`
  - `risk_random_forest.joblib`
  - `risk_metadata.json` (optional)

### Installation

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

#### Frontend Setup

```bash
cd frontend
npm install
```

### Running the System

1. **Start Backend** (Terminal 1):
```bash
cd backend
python main.py
```

Server runs on: http://127.0.0.1:8000

2. **Start Frontend** (Terminal 2):
```bash
cd frontend
npm run dev
```

Frontend runs on: http://localhost:5173

3. **Open Browser**: Navigate to http://localhost:5173

## 📁 Project Structure

```
Dermasense/
├── backend/
│   ├── main.py              # FastAPI server + ML inference
│   ├── models/              # Your trained models
│   │   ├── risk_cnn_densenet201.h5
│   │   ├── risk_random_forest.joblib
│   │   └── risk_metadata.json
│   ├── uploads/             # Uploaded images (auto-created)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── views/           # Vue pages
│   │   ├── components/      # Vue components
│   │   ├── router/          # Vue Router config
│   │   └── api/             # API client
│   └── package.json
└── README.md
```

## 🔬 How It Works

### 1. Image Analysis (ML Component)
- **Input**: Skin lesion image (299x299 RGB)
- **Process**: 
  - DenseNet201 extracts features
  - Random Forest classifies lesion patterns
  - Probabilities mapped to risk levels
- **Output**: Image risk probability (0-100%)

### 2. Rule-Based Scoring (Step 3)
- **Input**: User responses (duration, symptoms, location, etc.)
- **Process**: Rule-based scoring (NO ML)
- **Output**: Support risk score (0-100%)

### 3. Final Risk Calculation
```
Final Risk = (0.7 × Image Risk) + (0.3 × Support Risk)
```

### 4. Risk Level Assignment
- **LOW**: 0-40%
- **MEDIUM**: 41-65%
- **HIGH**: 66-100%

## 🎨 Features

- ✅ **Modern UI/UX** - Professional, responsive design
- ✅ **Image Upload & Analysis** - Drag-and-drop or file picker
- ✅ **Real-time Results** - Instant risk assessment display
- ✅ **Assessment History** - Track assessments over time
- ✅ **Monitoring Dashboard** - Visualize risk trends
- ✅ **PDF Reports** - Downloadable assessment reports
- ✅ **Educational Content** - ABCDE rule, photo tips, UV protection
- ✅ **Responsive Design** - Works on desktop and mobile

## 🔧 Configuration

### Backend Configuration

Edit `backend/main.py` to adjust:
- Model paths (lines 27-29)
- Risk thresholds (lines 56-57)
- Image size (line 31)
- Risk weights (lines 48-51)

### Frontend Configuration

Edit `frontend/src/api/client.js` to change:
- API base URL (default: http://127.0.0.1:8000)

## 📊 API Endpoints

### POST `/assess-risk`
Upload image and get risk assessment.

**Request:**
- `file`: Image file (multipart/form-data)
- `duration` (optional): Lesion duration
- `itching` (optional): Boolean
- `bleeding` (optional): Boolean
- `pain` (optional): Boolean
- `sun_exposure` (optional): High/Medium/Low
- `location` (optional): Lesion location

**Response:**
```json
{
  "success": true,
  "risk_level": "MEDIUM",
  "final_risk_score": 52.5,
  "final_risk_percentage": "52.5%",
  "image_risk": 55.0,
  "support_risk": 30.0,
  "explanations": [...],
  "recommendation": "...",
  "disclaimer": "..."
}
```

### GET `/assessments`
Get assessment history.

### GET `/assessments/{id}`
Get specific assessment.

## 🐛 Troubleshooting

### Models not loading:
- Verify model files are in `backend/models/`
- Check file permissions
- Run `python backend/test_models.py` to test model loading

### Backend won't start:
- Check Python version: `python --version` (need 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check for port conflicts (8000)

### Frontend won't start:
- Check Node version: `node --version` (need 16+)
- Install dependencies: `npm install`
- Clear cache: `rm -rf node_modules package-lock.json && npm install`

### Images not analyzing:
- Check backend console for errors
- Verify image format (JPG, PNG)
- Check file size (not too large)

## 📝 Development Notes

- **No database** - Assessments stored in memory (resets on restart)
- **Model loading** - Models loaded on server startup
- **Image storage** - Images saved in `backend/uploads/`
- **CORS** - Enabled for all origins (development mode)

## 🎓 For Thesis/Documentation

The system includes:
- Complete source code
- Model integration
- Professional UI/UX
- Error handling
- Logging and monitoring
- Documentation

## 📄 License

This project is for educational/research purposes.

## 👤 Author

Developed for thesis project: "DermaSense: A Machine Learning–Assisted Skin Lesion Risk Assessment and Monitoring System"

---

**System Status**: ✅ Fully Functional
**Last Updated**: December 2024
