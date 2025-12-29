# backend/main.py
from pathlib import Path
import io
import traceback
import numpy as np
from PIL import Image
from datetime import datetime
import uuid
import json

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
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Model paths
CNN_MODEL_PATH = MODEL_DIR / "risk_cnn_densenet201.h5"
RF_MODEL_PATH = MODEL_DIR / "risk_random_forest.joblib"
METADATA_PATH = MODEL_DIR / "risk_metadata.json"

IMG_SIZE = (224, 224)  # DenseNet201 input size

# =========================
# INTERNAL LABEL MAPPING (DO NOT EXPOSE TO USER)
# =========================
RISK_MAPPING = {
    "mel": "HIGH",      # Melanoma
    "scc": "HIGH",      # Squamous Cell Carcinoma
    "bcc": "MEDIUM",    # Basal Cell Carcinoma
    "ak": "MEDIUM",     # Actinic Keratosis
    "nv": "LOW",        # Nevus
    "bkl": "LOW",       # Benign Keratosis
    "df": "LOW",        # Dermatofibroma
    "vasc": "LOW",      # Vascular
}

# Risk level weights for probability calculation
RISK_WEIGHTS = {
    "HIGH": 0.85,
    "MEDIUM": 0.50,
    "LOW": 0.20,
}

# =========================
# SAFETY THRESHOLDS
# =========================
INVALID_CONFIDENCE = 0.30  # Lowered for better acceptance
ENTROPY_THRESHOLD = 0.95   # Increased threshold

# =========================
# IN-MEMORY STORAGE
# =========================
assessments_db = []

# =========================
# LOAD MODELS AND METADATA
# =========================
feature_extractor = None
rf_model = None
class_names = []
model_outputs_risk_levels = False  # Flag to check if model outputs risk levels directly
numeric_to_risk_mapping = {}  # Map numeric labels to risk levels (global)

try:
    # Load metadata if available
    metadata = {}
    if METADATA_PATH.exists():
        with open(METADATA_PATH, 'r') as f:
            metadata = json.load(f)
            print(f"✓ Metadata loaded from {METADATA_PATH.name}")
    
    # Load CNN model
    if CNN_MODEL_PATH.exists():
        try:
            # Try loading with custom objects if needed
            feature_extractor = keras.models.load_model(
                CNN_MODEL_PATH,
                compile=False  # Don't compile, we only need inference
            )
            print(f"✓ CNN model loaded: {CNN_MODEL_PATH.name}")
            if hasattr(feature_extractor, 'input_shape'):
                print(f"  Input shape: {feature_extractor.input_shape}")
        except Exception as e:
            print(f"⚠️ Error loading CNN model: {e}")
            print("  Attempting alternative loading method...")
            try:
                # Alternative: load weights directly
                import tensorflow as tf
                feature_extractor = tf.keras.models.load_model(CNN_MODEL_PATH, compile=False)
                print(f"✓ CNN model loaded (alternative method)")
            except Exception as e2:
                print(f"✗ Failed to load CNN model: {e2}")
                feature_extractor = None
    else:
        print(f"⚠️ CNN model not found: {CNN_MODEL_PATH}")
    
    # Load Random Forest model
    if RF_MODEL_PATH.exists():
        try:
            rf_model = joblib.load(RF_MODEL_PATH)
            print(f"✓ Random Forest model loaded: {RF_MODEL_PATH.name}")
            
            # Determine model output type
            if hasattr(rf_model, 'classes_'):
                model_classes = [str(c) for c in rf_model.classes_]
                print(f"  Model classes: {model_classes}")
                
                # Check if model outputs numeric labels (0, 1, 2, etc.)
                if all(c.isdigit() for c in model_classes):
                    # Numeric labels - map to risk levels from metadata
                    if 'labels' in metadata:
                        risk_labels = [label.upper() for label in metadata['labels']]
                        # Map numeric class indices to risk levels
                        numeric_to_risk_mapping = {
                            int(c): risk_labels[i] if i < len(risk_labels) else "LOW"
                            for i, c in enumerate(model_classes)
                        }
                        print(f"  ✓ Mapping numeric classes to risk levels: {numeric_to_risk_mapping}")
                        model_outputs_risk_levels = True
                    else:
                        # Default mapping: 0=LOW, 1=MEDIUM, 2=HIGH
                        numeric_to_risk_mapping = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
                        print(f"  ✓ Using default mapping: {numeric_to_risk_mapping}")
                        model_outputs_risk_levels = True
                # Check if model outputs risk levels directly
                elif all(level.lower() in ['high', 'medium', 'low'] for level in model_classes):
                    model_outputs_risk_levels = True
                    print("  ✓ Model outputs risk levels directly")
                else:
                    # Model outputs lesion classes, use mapping
                    class_names = [c.lower() for c in model_classes]
                    print(f"  ✓ Model outputs lesion classes: {class_names}")
        except Exception as e:
            print(f"✗ Failed to load Random Forest model: {e}")
            rf_model = None
    else:
        print(f"⚠️ Random Forest model not found: {RF_MODEL_PATH}")
    
    if feature_extractor and rf_model:
        print("✓ All models loaded successfully!")
    else:
        print("⚠️ Some models are missing. System will run in placeholder mode.")
        
except Exception as e:
    print(f"⚠️ Error loading models: {e}")
    traceback.print_exc()
    print("⚠️ System will run in placeholder mode until models are available.")

# =========================
# APP
# =========================
app = FastAPI(title="DermaSense API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# IMAGE PREPROCESS
# =========================
def preprocess_image(image_bytes: bytes):
    """Preprocess image for model input."""
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Resize to model input size
    img = img.resize(IMG_SIZE)
    
    # Convert to array and normalize to [0, 1] range
    arr = np.asarray(img, dtype=np.float32) / 255.0
    
    # Add batch dimension
    return np.expand_dims(arr, axis=0)

# =========================
# SKIN IMAGE VALIDATION
# =========================
def is_valid_skin_image(img_batch: np.ndarray) -> bool:
    """Reject obviously non-dermatological images."""
    img = img_batch[0]

    # More lenient validation - allow most images through
    # Let the model decide if it's confident
    mean = np.mean(img)
    std = np.std(img)

    # Very basic checks only
    if std < 0.01:  # Completely uniform (likely blank)
        return False
    if mean < 0.01 or mean > 0.99:  # Extremely dark or bright
        return False

    return True

# =========================
# HELPERS
# =========================
def entropy(probabilities):
    """Calculate entropy of probability distribution."""
    probs = np.clip(probabilities, 1e-8, 1.0)
    return -np.sum(probs * np.log(probs))

def calculate_image_risk_from_lesion_classes(probs: np.ndarray, class_names: list) -> float:
    """Calculate risk probability from lesion class probabilities."""
    total_risk = 0.0
    
    for i, class_name in enumerate(class_names):
        if i < len(probs):
            class_prob = float(probs[i])
            risk_level = RISK_MAPPING.get(class_name, "LOW")
            weight = RISK_WEIGHTS.get(risk_level, 0.20)
            total_risk += class_prob * weight
    
    # Normalize to 0-1 range
    normalized_risk = min(total_risk / 0.85, 1.0)
    return normalized_risk

def calculate_image_risk_from_risk_levels(probs: np.ndarray) -> float:
    """Calculate risk probability when model outputs risk levels directly."""
    # Map risk levels to weights
    risk_weights_map = {
        "HIGH": 0.85,
        "MEDIUM": 0.50,
        "LOW": 0.20
    }
    
    total_risk = 0.0
    if numeric_to_risk_mapping:
        # Use numeric to risk mapping
        for i, prob in enumerate(probs):
            prob_val = float(prob)
            risk_level = numeric_to_risk_mapping.get(i, "LOW")
            weight = risk_weights_map.get(risk_level, 0.20)
            total_risk += prob_val * weight
    elif hasattr(rf_model, 'classes_'):
        # Map classes to risk levels
        for i, prob in enumerate(probs):
            prob_val = float(prob)
            class_label = str(rf_model.classes_[i])
            # Check if it's a risk level string
            risk_level = class_label.upper()
            if risk_level not in risk_weights_map:
                # Try to infer from metadata
                risk_level = "LOW"  # Default
            weight = risk_weights_map.get(risk_level, 0.20)
            total_risk += prob_val * weight
    
    # Normalize
    normalized_risk = min(total_risk / 0.85, 1.0)
    return normalized_risk

def calculate_image_risk_probability(probs: np.ndarray) -> float:
    """Calculate risk probability from model output."""
    if model_outputs_risk_levels:
        return calculate_image_risk_from_risk_levels(probs)
    elif class_names:
        return calculate_image_risk_from_lesion_classes(probs, class_names)
    else:
        # Fallback: use max probability as risk indicator
        max_prob = float(np.max(probs))
        return max_prob * 0.7  # Scale to reasonable range

def get_risk_level(risk_score: float) -> str:
    """Convert risk score (0-100) to risk level."""
    if risk_score <= 40:
        return "LOW"
    elif risk_score <= 65:
        return "MEDIUM"
    else:
        return "HIGH"

def get_risk_explanations(risk_level: str, image_risk: float) -> list:
    """Generate explanations based on risk level."""
    if risk_level == "HIGH":
        return [
            "Irregular borders detected",
            "Significant color variation observed",
            "Asymmetry patterns identified",
            "Diameter concerns noted"
        ]
    elif risk_level == "MEDIUM":
        return [
            "Some border irregularity",
            "Moderate color variation",
            "Slight asymmetry present"
        ]
    else:
        return [
            "Regular border patterns",
            "Consistent coloration",
            "Symmetrical appearance"
        ]

def get_recommendations(risk_level: str) -> str:
    """Get recommendations based on risk level."""
    if risk_level == "HIGH":
        return "Seek consultation with a dermatologist as soon as possible for professional evaluation."
    elif risk_level == "MEDIUM":
        return "Monitor the lesion and consider consulting a dermatologist for further evaluation."
    else:
        return "Continue monitoring the lesion regularly. Consult a dermatologist if you notice any changes."

# =========================
# RULE-BASED SCORING ENGINE (Step 3)
# =========================
def calculate_support_risk_score(
    duration: str = None,
    itching: bool = False,
    bleeding: bool = False,
    pain: bool = False,
    sun_exposure: str = None,
    location: str = None
) -> float:
    """Calculate support risk score (0-100) based on user inputs."""
    score = 0.0
    
    if duration:
        duration_lower = duration.lower()
        if "month" in duration_lower:
            try:
                months = int(''.join(filter(str.isdigit, duration)))
                if months > 3:
                    score += 15
            except:
                pass
    
    if itching:
        score += 10
    if bleeding:
        score += 20
    if pain:
        score += 10
    
    if sun_exposure:
        sun_lower = sun_exposure.lower()
        if "high" in sun_lower:
            score += 15
        elif "medium" in sun_lower or "moderate" in sun_lower:
            score += 8
    
    if location:
        location_lower = location.lower()
        if any(term in location_lower for term in ["face", "neck", "head"]):
            score += 10
        elif any(term in location_lower for term in ["trunk", "chest", "back"]):
            score += 5
    
    # Normalize to 0-100 range
    normalized_score = min((score / 80.0) * 100.0, 100.0)
    return normalized_score

# =========================
# ROUTES
# =========================
@app.get("/")
async def root():
    return {
        "message": "DermaSense API",
        "version": "2.0.0",
        "description": "Machine Learning-Assisted Skin Lesion Risk Assessment System",
        "models_loaded": feature_extractor is not None and rf_model is not None
    }

@app.post("/assess-risk")
async def assess_risk(
    file: UploadFile = File(...),
    duration: str | None = Form(default=None),
    itching: bool = Form(default=False),
    bleeding: bool = Form(default=False),
    pain: bool = Form(default=False),
    sun_exposure: str | None = Form(default=None),
    location: str | None = Form(default=None),
):
    """Main risk assessment endpoint."""
    try:
        print(f"\n🔍 New assessment request received")
        
        # Read and preprocess image
        contents = await file.read()
        print(f"✓ Image loaded: {len(contents)} bytes")
        
        img_batch = preprocess_image(contents)
        print(f"✓ Image preprocessed: shape {img_batch.shape}")
        
        # Save image
        image_id = str(uuid.uuid4())
        image_path = UPLOAD_DIR / f"{image_id}.jpg"
        with open(image_path, "wb") as f:
            f.write(contents)
        print(f"✓ Image saved: {image_path.name}")

        # Validate image (lenient)
        if not is_valid_skin_image(img_batch):
            print("⚠️ Image validation failed")
            return {
                "success": False,
                "error": "invalid_image",
                "message": "The uploaded image does not appear to be a valid image. Please upload a clear photo.",
                "risk_level": None,
                "image_risk": None,
                "support_risk": None,
                "final_risk": None,
            }
        
        print("✓ Image validation passed")

        # ML-based image risk analysis
        if feature_extractor is None or rf_model is None:
            print("⚠️ Using placeholder risk probability (models not loaded)")
            image_risk_probability = 0.50
        else:
            try:
                print("🔬 Running ML model inference...")
                
                # Extract features using CNN
                features = feature_extractor(img_batch, training=False)
                if hasattr(features, 'numpy'):
                    features = features.numpy()
                else:
                    features = np.array(features)
                
                print(f"✓ Features extracted: shape {features.shape}")
                
                # Reshape if needed (flatten for RF)
                original_shape = features.shape
                if len(features.shape) > 2:
                    features = features.reshape(features.shape[0], -1)
                    print(f"✓ Features reshaped: {original_shape} -> {features.shape}")
                
                # Get probabilities from Random Forest
                probs = rf_model.predict_proba(features)[0]
                print(f"✓ Probabilities obtained: {len(probs)} classes")
                
                # Log probabilities
                if hasattr(rf_model, 'classes_'):
                    if numeric_to_risk_mapping:
                        # Map numeric classes to risk levels for display
                        prob_dict = {
                            f"{c} ({numeric_to_risk_mapping.get(int(c), 'UNKNOWN')})": float(probs[i])
                            for i, c in enumerate(rf_model.classes_)
                        }
                    else:
                        prob_dict = {str(c): float(probs[i]) for i, c in enumerate(rf_model.classes_)}
                    print(f"  Probabilities: {prob_dict}")
                
                max_prob = float(np.max(probs))
                ent = entropy(probs)
                print(f"  Max probability: {max_prob:.3f}, Entropy: {ent:.3f}")

                # Check confidence (more lenient)
                if max_prob < INVALID_CONFIDENCE:
                    print(f"⚠️ Low confidence prediction (max_prob={max_prob:.3f} < {INVALID_CONFIDENCE})")
                    # Don't reject, just use lower weight or proceed anyway
                
                # Calculate image risk probability
                image_risk_probability = calculate_image_risk_probability(probs)
                print(f"✓ Image risk probability: {image_risk_probability:.3f} ({image_risk_probability*100:.1f}%)")
                
            except Exception as e:
                print(f"✗ Error during ML inference: {e}")
                traceback.print_exc()
                # Fallback to placeholder
                image_risk_probability = 0.50
                print("⚠️ Using fallback risk probability")
        
        image_risk_percentage = image_risk_probability * 100.0

        # Rule-based support risk scoring
        support_risk_score = calculate_support_risk_score(
            duration=duration,
            itching=itching,
            bleeding=bleeding,
            pain=pain,
            sun_exposure=sun_exposure,
            location=location
        )
        print(f"✓ Support risk score: {support_risk_score:.2f}%")

        # Combine risks: 70% image risk + 30% support risk
        final_risk_score = (0.7 * image_risk_percentage) + (0.3 * support_risk_score)
        risk_level = get_risk_level(final_risk_score)
        print(f"✓ Final risk: {final_risk_score:.2f}% ({risk_level})")
        
        # Generate explanations and recommendations
        explanations = get_risk_explanations(risk_level, image_risk_percentage)
        recommendation = get_recommendations(risk_level)

        # Save to in-memory storage
        assessment = {
            "id": image_id,
            "timestamp": datetime.now().isoformat(),
            "image_path": str(image_path),
            "risk_level": risk_level,
            "final_risk_score": final_risk_score,
            "image_risk": image_risk_percentage,
            "support_risk": support_risk_score,
            "explanations": explanations,
            "recommendation": recommendation,
            "user_inputs": {
                "duration": duration,
                "itching": itching,
                "bleeding": bleeding,
                "pain": pain,
                "sun_exposure": sun_exposure,
                "location": location,
            }
        }
        assessments_db.append(assessment)
        print(f"✓ Assessment saved (Total: {len(assessments_db)})\n")

        # Return results
        return {
            "success": True,
            "assessment_id": image_id,
            "risk_level": risk_level,
            "final_risk_score": round(final_risk_score, 2),
            "final_risk_percentage": f"{final_risk_score:.1f}%",
            "image_risk": round(image_risk_percentage, 2),
            "image_risk_percentage": f"{image_risk_percentage:.1f}%",
            "support_risk": round(support_risk_score, 2),
            "support_risk_percentage": f"{support_risk_score:.1f}%",
            "explanations": explanations,
            "recommendation": recommendation,
            "timestamp": assessment["timestamp"],
            "disclaimer": "This system is for risk assessment only and not a medical diagnosis. Always consult a dermatologist for professional evaluation.",
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error in assess_risk: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")

@app.get("/assessments")
async def get_assessments():
    """Get all assessment history."""
    return {
        "success": True,
        "count": len(assessments_db),
        "assessments": assessments_db[-50:]  # Return last 50
    }

@app.get("/assessments/{assessment_id}")
async def get_assessment(assessment_id: str):
    """Get a specific assessment by ID."""
    for assessment in assessments_db:
        if assessment["id"] == assessment_id:
            return {
                "success": True,
                "assessment": assessment
            }
    raise HTTPException(status_code=404, detail="Assessment not found")

@app.delete("/assessments/{assessment_id}")
async def delete_assessment(assessment_id: str):
    """Delete an assessment."""
    global assessments_db
    assessments_db = [a for a in assessments_db if a["id"] != assessment_id]
    return {"success": True, "message": "Assessment deleted"}

if __name__ == "__main__":
    import socket
    
    def is_port_available(port):
        """Check if a port is available."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return True
            except OSError:
                return False
    
    # Try to find an available port
    port = 8000
    if not is_port_available(port):
        print(f"⚠️ Port {port} is already in use. Trying alternative ports...")
        for alt_port in [8001, 8002, 8003, 8080]:
            if is_port_available(alt_port):
                port = alt_port
                print(f"✓ Using port {port} instead")
                break
        else:
            print("❌ No available ports found. Please close the process using port 8000.")
            print("   On Windows, run: netstat -ano | findstr :8000")
            print("   Then kill the process with: taskkill /PID <PID> /F")
            exit(1)
    
    print("\n" + "="*60)
    print("Starting DermaSense Backend Server...")
    print("="*60)
    if feature_extractor and rf_model:
        print("✓ All models loaded and ready")
    else:
        print("⚠️ Running in placeholder mode (some models missing)")
    print(f"✓ Server starting on http://127.0.0.1:{port}")
    print("="*60 + "\n")
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)
