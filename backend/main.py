from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from pathlib import Path
from typing import Tuple, Dict
import os
import shutil
import io

import numpy as np
from PIL import Image
import joblib

# -------------------------
# Paths & model setup
# -------------------------

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "dermasense_model.pkl"  # your trained model later

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL = None  # will hold your trained classifier (when available)


def load_model():
    """
    Try to load a trained model from disk.
    For now this is optional – the API will still run with a dummy model.
    """
    global MODEL
    if MODEL_PATH.exists():
        try:
            MODEL = joblib.load(MODEL_PATH)
            print(f"[DermaSense] Loaded model from {MODEL_PATH}")
        except Exception as exc:
            print(f"[DermaSense] Failed to load model: {exc}")
            MODEL = None
    else:
        print("[DermaSense] No model file found, using dummy predictions.")


load_model()

# -------------------------
# FastAPI app
# -------------------------

app = FastAPI(
    title="DermaSense API",
    description="Backend for skin lesion analysis (Benign / BCC / SCC)",
    version="1.0.0",
)

# Allow your Vue frontend to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later: restrict to ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expose uploads as static files so frontend can show the original image
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/")
def root():
    return {"message": "DermaSense API is running"}


# -------------------------
# Utility functions
# -------------------------


CLASS_NAMES = [
    "No Skin Cancer (Benign)",
    "Basal Cell Carcinoma (BCC)",
    "Squamous Cell Carcinoma (SCC)",
]


def preprocess_image(file_bytes: bytes, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """
    Convert raw image bytes into a normalized numpy array suitable for a model.
    """
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    image = image.resize(target_size)
    arr = np.array(image).astype("float32") / 255.0  # normalize 0–1
    arr = np.expand_dims(arr, axis=0)  # shape: (1, H, W, C)
    return arr


def dummy_predict(arr: np.ndarray) -> np.ndarray:
    """
    Fallback prediction if no trained model is loaded.
    Returns a 1x3 array of probabilities that sum to 1.
    Here we use a simple heuristic + fixed scores just so the API works.
    """
    # Example: simple fixed probabilities (you can randomize if you want)
    probs = np.array([[0.60, 0.25, 0.15]], dtype="float32")
    return probs


def predict_image(file_bytes: bytes) -> Tuple[str, float, Dict[str, float]]:
    """
    Run the image through the model (or dummy predictor) and return:
    - predicted label
    - confidence (0–1)
    - dictionary of probabilities per class
    """
    arr = preprocess_image(file_bytes)

    if MODEL is not None:
        # Example for a scikit-learn-style model that expects features:
        # features = feature_extractor(arr)  # <-- YOU will implement this later
        # probs = MODEL.predict_proba(features)  # shape: (1, 3)
        # For now, still use dummy until you connect your real pipeline
        probs = dummy_predict(arr)
    else:
        probs = dummy_predict(arr)

    probs = probs[0]
    best_idx = int(np.argmax(probs))
    best_label = CLASS_NAMES[best_idx]
    best_conf = float(probs[best_idx])

    prob_dict = {
        CLASS_NAMES[i]: float(round(float(p), 4)) for i, p in enumerate(probs)
    }

    return best_label, best_conf, prob_dict


def build_explanation(label: str) -> str:
    """
    Small, high-level explanation for each class.
    NOTE: Wording is intentionally cautious for safety.
    """
    if "Basal Cell" in label:
        return (
            "The pattern is most consistent with Basal Cell Carcinoma (BCC), "
            "a common non-melanoma skin cancer that often appears as a pearly "
            "or nodular lesion. This is only a screening result. "
            "Please consult a dermatologist for confirmation."
        )
    elif "Squamous Cell" in label:
        return (
            "The pattern is most consistent with Squamous Cell Carcinoma (SCC), "
            "a non-melanoma skin cancer that can appear as a scaly or crusted plaque. "
            "This is only a screening result. Please consult a dermatologist "
            "for confirmation and further evaluation."
        )
    else:
        return (
            "The lesion appears most consistent with a benign (non-cancerous) pattern "
            "based on the available image. However, this is not a diagnostic result. "
            "Any changing, symptomatic, or suspicious lesion should still be assessed "
            "by a dermatologist."
        )


# -------------------------
# Main analysis endpoint
# -------------------------


@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    age: str | None = Form(None),
    sex: str | None = Form(None),
    site: str | None = Form(None),
):
    """
    Analyze a skin lesion image and return:
    - predicted class (Benign / BCC / SCC)
    - confidence score
    - short explanation
    """
    # Read image bytes
    raw_bytes = await file.read()

    # Save a copy of the uploaded image so the frontend can show it
    save_path = UPLOAD_DIR / file.filename
    with open(save_path, "wb") as buffer:
        buffer.write(raw_bytes)

    # Run prediction
    label, confidence, prob_dict = predict_image(raw_bytes)
    explanation = build_explanation(label)

    # Build a human-friendly percent string
    confidence_pct = round(confidence * 100, 1)

    result = {
        "label": label,
        "confidence": confidence,  # 0–1
        "confidence_display": f"{confidence_pct:.1f}%",
        "description": explanation,
        "probabilities": prob_dict,
        "image_url": f"/uploads/{file.filename}",
        "meta": {
            "age": age,
            "sex": sex,
            "site": site,
        },
        "disclaimer": (
            "DermaSense is a research prototype and does not provide a medical "
            "diagnosis. All results are for decision support only and must be "
            "confirmed by a qualified dermatologist."
        ),
    }

    return JSONResponse(content=result)
