# backend/main.py
from pathlib import Path
import io
import traceback

import numpy as np
from PIL import Image

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware

from tensorflow import keras
import joblib
import uvicorn

# =========================
# PATHS & CONSTANTS
# =========================
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(exist_ok=True)

CNN_MODEL_PATH = MODEL_DIR / "cnn_densenet201_feature_extractor.h5"
RF_MODEL_PATH = MODEL_DIR / "rf_densenet201_bcc_scc.pkl"
CLASS_NAMES_PATH = MODEL_DIR / "class_names.npy"

IMG_SIZE = (299, 299)  # must match your training notebook

# If model confidence (max probability) is below this,
# we will return "No non-melanoma cancer has found".
NO_CANCER_CONFIDENCE_THRESHOLD = 0.55  # 55% – you can tune this

# =========================
# LOAD MODELS AT STARTUP
# =========================
print(" Loading CNN feature extractor from:", CNN_MODEL_PATH)
if not CNN_MODEL_PATH.exists():
    raise RuntimeError(f"CNN model not found at {CNN_MODEL_PATH}")
feature_extractor = keras.models.load_model(CNN_MODEL_PATH)

print(" Loading Random Forest classifier from:", RF_MODEL_PATH)
if not RF_MODEL_PATH.exists():
    raise RuntimeError(f"Random Forest model not found at {RF_MODEL_PATH}")
rf_model = joblib.load(RF_MODEL_PATH)

print(" Loading class names from:", CLASS_NAMES_PATH)
if not CLASS_NAMES_PATH.exists():
    raise RuntimeError(f"Class names file not found at {CLASS_NAMES_PATH}")
class_names = np.load(CLASS_NAMES_PATH, allow_pickle=True).tolist()
class_names = [str(c) for c in class_names]
print("   Classes:", class_names)

# Safety check: CNN feature dimension must match RF
print(" Checking feature dimensions...")
dummy = np.zeros((1,) + IMG_SIZE + (3,), dtype=np.float32)
dummy_features = feature_extractor(dummy).numpy()
feature_dim = dummy_features.shape[1]
print("   CNN feature dimension:", feature_dim)
if hasattr(rf_model, "n_features_in_"):
    print("   RF expects n_features_in_:", rf_model.n_features_in_)
    if rf_model.n_features_in_ != feature_dim:
        raise RuntimeError(
            f"Feature dimension mismatch: CNN produces {feature_dim} features, "
            f"but RandomForest expects {rf_model.n_features_in_}. "
            f"Retrain RF using this feature_extractor or load the matching CNN."
        )

# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="Dermasense Skin Cancer Classifier",
    description=(
        "DenseNet201 (CNN) feature extractor + Random Forest classifier "
        "for Basal Cell Carcinoma (BCC) and Squamous Cell Carcinoma (SCC)."
    ),
    version="1.0.0",
)

# Allow your Vue dev server (localhost:5173, etc.) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for dev; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# IMAGE PREPROCESSING
# =========================
def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Convert uploaded bytes into tensor (1, 299, 299, 3) in 0–255 range.
    The internal Rescaling(1/255) layer in feature_extractor will handle
    normalization, just like during training.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        print(" Error opening image:", e)
        raise HTTPException(status_code=400, detail="Invalid image file")

    img = img.resize(IMG_SIZE)
    # IMPORTANT: do NOT divide by 255 here; feature_extractor already does that
    img_array = np.asarray(img, dtype=np.float32)  # values 0–255
    img_array = np.expand_dims(img_array, axis=0)  # shape (1, H, W, 3)
    return img_array


# =========================
# ENDPOINTS
# =========================
@app.get("/")
def root():
    return {
        "message": "Dermasense Skin Cancer Classifier API is running.",
        "classes": class_names,
    }


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    age: str | None = Form(default=None),
    sex: str | None = Form(default=None),
    site: str | None = Form(default=None),
):
    """
    Predict BCC/SCC for uploaded image.
    Returns:
      - label: human-readable label (what your ResultPage uses)
      - description: short explanation
      - confidence: max probability (0–1)
      - confidence_display: formatted percentage string
      - prediction_type: 'lesion' or 'none'
      - predicted_label: 'bcc', 'scc', or 'none'
      - message: summary text
    """
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded.")

        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # Save the upload for audit/logging (optional)
        save_path = UPLOAD_DIR / file.filename
        with open(save_path, "wb") as f:
            f.write(contents)

        # 1. Preprocess
        try:
            img_batch = preprocess_image(contents)
        except HTTPException:
            raise
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=400, detail=f"Image preprocessing error: {e}")

        # 2. CNN feature extraction
        try:
            features = feature_extractor(img_batch, training=False).numpy()
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Feature extractor error: {e}")

        # 3. Random Forest prediction
        try:
            pred_idx = int(rf_model.predict(features)[0])
            proba = rf_model.predict_proba(features)[0]
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Random Forest error: {e}")

        if pred_idx < 0 or pred_idx >= len(class_names):
            raise HTTPException(status_code=500, detail="Invalid prediction index from RF.")

        max_proba = float(np.max(proba))  # 0–1
        confidence_display = f"{max_proba * 100:.2f}%"

        # 4. Decide final label & description
        if max_proba < NO_CANCER_CONFIDENCE_THRESHOLD:
            prediction_type = "none"
            predicted_label = "none"
            label = "No Skin Cancer (Benign)"
            description = (
                "The model did not find strong evidence of basal cell carcinoma "
                "or squamous cell carcinoma in this image. This does NOT replace a clinical "
                "examination. Please consult a dermatologist if there are any concerns."
            )
            message = "No non-melanoma cancer has found."
        else:
            prediction_type = "lesion"
            predicted_label = class_names[pred_idx]

            if predicted_label.lower() == "bcc":
                label = "Basal Cell Carcinoma (BCC)"
                description = (
                    "Findings are more consistent with Basal Cell Carcinoma (BCC), a common "
                    "type of non-melanoma skin cancer that usually grows slowly and rarely spreads. "
                    "Early dermatologic evaluation and treatment are important."
                )
            elif predicted_label.lower() == "scc":
                label = "Squamous Cell Carcinoma (SCC)"
                description = (
                    "Findings are more consistent with Squamous Cell Carcinoma (SCC), a type of "
                    "non-melanoma skin cancer that can sometimes grow more aggressively. Prompt "
                    "assessment by a dermatologist is recommended."
                )
            else:
                # Fallback – should not happen if class_names = ['bcc','scc']
                label = predicted_label
                description = (
                    "The model detected a lesion pattern, but the class label is unexpected. "
                    "Please confirm the class mapping in the system."
                )

            message = f"Model suggests {label} with {confidence_display} confidence."

        prob_dict = {class_names[i]: float(proba[i]) for i in range(len(class_names))}

        clinical_info = {
            "age": age,
            "sex": sex,
            "site": site,
        }

        return {
            "filename": file.filename,
            "prediction_type": prediction_type,   # 'lesion' or 'none'
            "predicted_label": predicted_label,   # 'bcc' / 'scc' / 'none'
            "label": label,                       # used directly in ResultPage
            "description": description,           # used directly in ResultPage
            "confidence": max_proba,              # 0–1
            "confidence_display": confidence_display,
            "probabilities": prob_dict,
            "message": message,
            "clinical_info": clinical_info,
            "image_url": None,                    # frontend will fill from preview
        }

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
