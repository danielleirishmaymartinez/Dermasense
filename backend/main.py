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
# PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

CNN_MODEL_PATH = MODEL_DIR / "cnn_densenet201_feature_extractor.h5"
RF_MODEL_PATH = MODEL_DIR / "rf_densenet201_bcc_scc.pkl"
CLASS_NAMES_PATH = MODEL_DIR / "class_names.npy"

IMG_SIZE = (299, 299)

# =========================
# LOAD MODELS
# =========================
feature_extractor = keras.models.load_model(CNN_MODEL_PATH)
rf_model = joblib.load(RF_MODEL_PATH)
class_names = np.load(CLASS_NAMES_PATH, allow_pickle=True).tolist()

# =========================
# FASTAPI APP
# =========================
app = FastAPI(title="DermaSense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# IMAGE PREPROCESSING
# =========================
def preprocess_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = np.asarray(img, dtype=np.float32)
    return np.expand_dims(arr, axis=0)


# =========================
# STRONG IMAGE VALIDATION
# =========================
def is_valid_skin_image(img_batch: np.ndarray) -> bool:
    """
    Reject obvious non-skin images (cartoons, posters, objects).
    CODE-ONLY validation.
    """
    img = img_batch[0]

    mean = np.mean(img)
    std = np.std(img)

    # Cartoons & posters are usually:
    # - Very colorful
    # - High contrast
    # - Very clean edges

    if std > 70:        # too colorful
        return False
    if mean < 50:       # too dark
        return False
    if mean > 210:      # too bright / white bg
        return False

    return True


# =========================
# API
# =========================
@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    age: str | None = Form(default=None),
    sex: str | None = Form(default=None),
    site: str | None = Form(default=None),
):
    try:
        contents = await file.read()

        # 1️⃣ PREPROCESS
        img_batch = preprocess_image(contents)

        # 2️⃣ HARD STOP — INVALID IMAGE
        if not is_valid_skin_image(img_batch):
            return {
                "prediction_type": "invalid",
                "predicted_label": "invalid",
                "label": "Invalid Image",
                "description": (
                    "The uploaded image is not related to Basal Cell Carcinoma (BCC) "
                    "or Squamous Cell Carcinoma (SCC) skin lesions.\n\n"
                ),
                "confidence": 0.0,
                "confidence_display": "N/A",
                "probabilities": {},
                "message": "Image rejected.",
                "clinical_info": {
                    "age": age,
                    "sex": sex,
                    "site": site,
                }
            }

        # 3️⃣ FEATURE EXTRACTION
        features = feature_extractor(img_batch, training=False).numpy()

        # 4️⃣ RF PREDICTION
        pred_idx = int(rf_model.predict(features)[0])
        proba = rf_model.predict_proba(features)[0]
        max_proba = float(np.max(proba))

        # 5️⃣ LOW CONFIDENCE BLOCK
        if max_proba < 0.55:
            return {
                "prediction_type": "none",
                "predicted_label": "none",
                "label": "Uncertain Classification",
                "description": (
                    "The image appears to be a skin lesion, but the system "
                    "cannot confidently classify it as BCC or SCC."
                ),
                "confidence": max_proba,
                "confidence_display": f"{max_proba * 100:.2f}%",
                "probabilities": {},
                "message": "Low confidence result.",
                "clinical_info": {
                    "age": age,
                    "sex": sex,
                    "site": site,
                }
            }

        predicted = class_names[pred_idx]

        return {
            "prediction_type": "lesion",
            "predicted_label": predicted,
            "label": "Basal Cell Carcinoma (BCC)" if predicted == "bcc" else "Squamous Cell Carcinoma (SCC)",
            "description": "Consult a dermatologist for confirmation.",
            "confidence": max_proba,
            "confidence_display": f"{max_proba * 100:.2f}%",
            "probabilities": {
                class_names[i]: float(proba[i]) for i in range(len(class_names))
            },
            "message": "Prediction completed.",
            "clinical_info": {
                "age": age,
                "sex": sex,
                "site": site,
            }
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)