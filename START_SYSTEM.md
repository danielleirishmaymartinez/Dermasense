# 🚀 Starting Your DermaSense System

## Step 1: Start the Backend Server

Open a terminal and run:

```bash
cd backend
python main.py
```

**Expected output:**
```
============================================================
Starting DermaSense Backend Server...
============================================================
✓ Metadata loaded from risk_metadata.json
✓ CNN model loaded: risk_cnn_densenet201.h5
✓ Random Forest model loaded: risk_random_forest.joblib
✓ All models loaded successfully!
✓ Server starting on http://127.0.0.1:8000
============================================================
```

**If you see errors:**
- Make sure all model files are in `backend/models/`:
  - `risk_cnn_densenet201.h5`
  - `risk_random_forest.joblib`
  - `risk_metadata.json` (optional)
- Install dependencies: `pip install -r requirements.txt`
- Check TensorFlow version compatibility

## Step 2: Start the Frontend

Open a **NEW terminal** (keep backend running) and run:

```bash
cd frontend
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Step 3: Use the System

1. Open your browser and go to: **http://localhost:5173**
2. Click **"Get Started"** or go to **Dashboard**
3. Click **"New Risk Assessment"**
4. Upload a skin lesion image
5. Fill in optional information (Step 3)
6. Click **"Analyze Risk"**
7. View your results!

## ✅ Testing the System

### Test Image Upload:
- Use any skin lesion image (JPG, PNG)
- The system will:
  1. Validate the image
  2. Run ML analysis
  3. Calculate risk score
  4. Display results

### Check Backend Logs:
The backend will print detailed information:
```
🔍 New assessment request received
✓ Image loaded: 123456 bytes
✓ Image preprocessed: shape (1, 299, 299, 3)
✓ Image saved: abc123.jpg
✓ Image validation passed
🔬 Running ML model inference...
✓ Features extracted: shape (1, 2048)
✓ Probabilities obtained: 8 classes
  Probabilities: {'ak': 0.1, 'bcc': 0.2, ...}
✓ Image risk probability: 0.45 (45.0%)
✓ Support risk score: 20.00%
✓ Final risk: 37.50% (LOW)
✓ Assessment saved (Total: 1)
```

## 🔧 Troubleshooting

### Backend won't start:
- Check if models are in `backend/models/` folder
- Verify Python dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### Frontend won't start:
- Install dependencies: `npm install`
- Check Node.js version (16+ required)

### Images not analyzing:
- Check backend console for errors
- Verify model files are loaded correctly
- Check image format (JPG, PNG supported)

### "Models not loaded" warning:
- Verify model files exist
- Check file permissions
- Try running: `python test_models.py` in backend folder

## 📝 Notes

- **No database required** - Assessments stored in memory (resets on restart)
- **Model loading** - Models load on server startup (may take a few seconds)
- **Image storage** - Uploaded images saved in `backend/uploads/`
- **Timeout** - Image analysis may take 10-30 seconds depending on hardware

---

**Your system is ready! Start both servers and upload an image to test it!** 🎉

