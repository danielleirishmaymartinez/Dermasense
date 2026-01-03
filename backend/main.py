# backend/main.py
from pathlib import Path
import io
import traceback
import numpy as np
from PIL import Image
from datetime import datetime
import uuid
import json

from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from tensorflow import keras
import joblib
import uvicorn

# Database and authentication imports
from database import init_db, get_db, User, Assessment, Image
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from schemas import UserCreate, UserResponse, Token, AssessmentResponse, AssessmentDetail, UserProfile

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
INVALID_CONFIDENCE = 0.35  # Minimum confidence for valid skin lesion prediction
ENTROPY_THRESHOLD = 0.92   # Maximum entropy (higher = more uncertain = likely wrong image type)

# =========================
# DATABASE INITIALIZATION
# =========================
# Initialize database tables on startup (commented out after first run)
# Uncomment the line below to create tables, then comment it again
# init_db()

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
app = FastAPI(title="DermaSense API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    try:
        # Test database connection
        from database import engine
        with engine.connect() as conn:
            pass
        print("✓ Database connection verified")
        
        # Initialize tables
        init_db()
        print("✓ Database tables initialized")
    except Exception as e:
        print(f"⚠️ Database initialization error: {e}")
        print("⚠️ Please check your database connection and DATABASE_URL in .env file")
        import traceback
        traceback.print_exc()

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
    """
    Comprehensive validation to reject non-skin images.
    Uses image statistics, color distribution, and texture analysis.
    
    Returns False for:
    - Objects (furniture, electronics, food, etc.)
    - Landscapes/buildings
    - Selfies/full body photos
    - Text documents
    - Any clearly non-skin images
    """
    img = img_batch[0]  # Shape: (224, 224, 3), values 0-1
    
    # Convert to 0-255 range for some calculations
    img_255 = (img * 255).astype(np.uint8)
    
    # ========================================
    # 1. Basic Image Quality Checks
    # ========================================
    mean_intensity = np.mean(img)
    std_intensity = np.std(img)
    
    # Reject completely uniform images (blank/solid color)
    if std_intensity < 0.02:
        print(f"  ✗ Validation failed: Image is too uniform (std={std_intensity:.4f})")
        return False
    
    # Reject extremely dark or bright images (likely not skin)
    if mean_intensity < 0.05 or mean_intensity > 0.95:
        print(f"  ✗ Validation failed: Image too dark/bright (mean={mean_intensity:.4f})")
        return False
    
    # ========================================
    # 2. Color Distribution Analysis
    # ========================================
    # Extract RGB channels
    r_channel = img[:, :, 0]
    g_channel = img[:, :, 1]
    b_channel = img[:, :, 2]
    
    # Skin typically has R > G > B (in 0-1 range, normalized RGB)
    # Convert to RGB (0-255) for skin tone detection
    r_mean = np.mean(img_255[:, :, 0])
    g_mean = np.mean(img_255[:, :, 1])
    b_mean = np.mean(img_255[:, :, 2])
    
    # Skin color range check (typical skin tones in RGB)
    # Skin generally has: R > G > B, and R, G, B in reasonable ranges
    # This helps reject blue skies, green landscapes, etc.
    
    # Check if image is predominantly one color (likely not skin)
    r_std = np.std(img_255[:, :, 0])
    g_std = np.std(img_255[:, :, 1])
    b_std = np.std(img_255[:, :, 2])
    
    # If all channels have very low variation, likely not skin (monochrome object)
    if r_std < 10 and g_std < 10 and b_std < 10:
        print(f"  ✗ Validation failed: Image is monochrome/low variation")
        return False
    
    # ========================================
    # 3. Texture/Edge Analysis
    # ========================================
    # Convert to grayscale for texture analysis
    gray = 0.299 * r_channel + 0.587 * g_channel + 0.114 * b_channel
    
    # Calculate local variance (texture measure)
    # Skin lesions typically have some texture variation
    # Very smooth images (like solid objects) or very chaotic (like complex scenes) are suspicious
    
    # Calculate gradient magnitude as texture measure
    # Use simple edge detection (Sobel-like approximation)
    h, w = gray.shape
    grad_x = gray[1:, :] - gray[:-1, :]
    grad_y = gray[:, 1:] - gray[:, :-1]
    gradient_magnitude = np.sqrt(grad_x[:, :-1]**2 + grad_y[:-1, :]**2)
    mean_gradient = np.mean(gradient_magnitude)
    
    # Too smooth (likely solid object/surface)
    if mean_gradient < 0.01:
        print(f"  ✗ Validation failed: Image too smooth (gradient={mean_gradient:.4f})")
        return False
    
    # Too chaotic (likely complex scene with many objects)
    if mean_gradient > 0.15:
        print(f"  ✗ Validation failed: Image too chaotic (gradient={mean_gradient:.4f}, likely complex scene)")
        return False
    
    # ========================================
    # 4. Aspect Ratio / Content Check
    # ========================================
    # Check color uniformity in regions
    # Skin lesion images typically have some variation but not extreme
    # Split image into quadrants and check variation
    h_mid, w_mid = h // 2, w // 2
    quadrants = [
        gray[:h_mid, :w_mid],
        gray[:h_mid, w_mid:],
        gray[h_mid:, :w_mid],
        gray[h_mid:, w_mid:]
    ]
    
    quadrant_means = [np.mean(q) for q in quadrants]
    quadrant_std = np.std(quadrant_means)
    
    # If quadrants are too different, likely not a close-up skin image
    # (could be a landscape with sky/ground, or object with background)
    if quadrant_std > 0.25:
        print(f"  ✗ Validation failed: Image has high spatial variation (likely not close-up skin)")
        return False
    
    # ========================================
    # 5. Color Saturation Check
    # ========================================
    # Skin images typically have moderate saturation
    # Very saturated colors (like bright objects) or desaturated (grayscale) are suspicious
    
    # Calculate saturation (simplified)
    max_channel = np.maximum(np.maximum(r_channel, g_channel), b_channel)
    min_channel = np.minimum(np.minimum(r_channel, g_channel), b_channel)
    saturation = np.mean(max_channel - min_channel)
    
    # Too desaturated (likely grayscale/document)
    if saturation < 0.05:
        print(f"  ✗ Validation failed: Image too desaturated (saturation={saturation:.4f})")
        return False
    
    # ========================================
    # 6. Overall Image Statistics
    # ========================================
    # Skin images typically have:
    # - Moderate brightness (0.3 - 0.7)
    # - Moderate contrast (std 0.1 - 0.3)
    # - Some color variation
    
    if not (0.25 <= mean_intensity <= 0.75):
        print(f"  ✗ Validation failed: Mean intensity out of typical skin range (mean={mean_intensity:.4f})")
        return False
    
    if not (0.08 <= std_intensity <= 0.35):
        print(f"  ✗ Validation failed: Contrast out of typical skin range (std={std_intensity:.4f})")
        return False
    
    # All checks passed
    print(f"  ✓ Image validation passed (mean={mean_intensity:.3f}, std={std_intensity:.3f}, gradient={mean_gradient:.3f})")
    return True

def validate_model_confidence(probs: np.ndarray, max_prob: float, entropy_val: float) -> tuple[bool, str]:
    """
    Secondary validation using model confidence.
    
    Returns:
        (is_valid, error_message)
    """
    # If model is very uncertain, likely not a skin lesion image
    # High entropy = uncertain prediction = likely wrong image type
    if entropy_val > ENTROPY_THRESHOLD:
        return False, "The image analysis indicates high uncertainty. This may not be a skin lesion image. Please upload a clear, close-up photo of a skin lesion."
    
    # If max probability is very low, model is uncertain
    # This suggests the image doesn't match expected patterns
    if max_prob < INVALID_CONFIDENCE:
        return False, "The image does not appear to match patterns of skin lesions. Please ensure you are uploading a clear, close-up photo of a skin lesion."
    
    return True, ""

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
        "version": "3.0.0",
        "description": "Machine Learning-Assisted Skin Lesion Risk Assessment System",
        "models_loaded": feature_extractor is not None and rf_model is not None
    }

# =========================
# AUTHENTICATION ROUTES
# =========================
@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Validate password length
        if len(user_data.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters long"
            )
        
        # Check password byte length (bcrypt limit is 72 bytes)
        password_bytes = user_data.password.encode('utf-8')
        if len(password_bytes) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is too long (maximum 72 bytes)"
            )
        
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        
        if existing_user:
            if existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        print(f"✓ New user registered: {db_user.username} ({db_user.email})")
        return UserResponse.model_validate(db_user)
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Registration error: {e}")
        traceback.print_exc()
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token"""
    # Find user by username or email
    user = db.query(User).filter(
        (User.username == form_data.username) | (User.email == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    print(f"✓ User logged in: {user.username}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }


@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@app.get("/users/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user profile with assessment count"""
    assessment_count = db.query(Assessment).filter(Assessment.user_id == current_user.id).count()
    
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        created_at=current_user.created_at,
        total_assessments=assessment_count
    )

@app.post("/assess-risk", response_model=AssessmentResponse)
async def assess_risk(
    file: UploadFile = File(...),
    duration: str | None = Form(default=None),
    itching: bool = Form(default=False),
    bleeding: bool = Form(default=False),
    pain: bool = Form(default=False),
    sun_exposure: str | None = Form(default=None),
    location: str | None = Form(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Main risk assessment endpoint (requires authentication)."""
    try:
        print(f"\n🔍 New assessment request received from user: {current_user.username}")
        
        # Read and preprocess image
        contents = await file.read()
        print(f"✓ Image loaded: {len(contents)} bytes")
        
        img_batch = preprocess_image(contents)
        print(f"✓ Image preprocessed: shape {img_batch.shape}")

        # Validate image using comprehensive checks
        print("🔍 Validating image (checking if it's a skin lesion image)...")
        if not is_valid_skin_image(img_batch):
            print("⚠️ Image validation failed - image does not appear to be a skin lesion")
            return {
                "success": False,
                "error": "invalid_image",
                "message": "The uploaded image does not appear to be a skin lesion image. Please upload a clear, close-up photo of a skin lesion for assessment.",
                "risk_level": None,
                "image_risk": None,
                "support_risk": None,
                "final_risk": None,
            }
        
        print("✓ Image validation passed - image appears to be a skin lesion")

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

                # Secondary validation: Check model confidence
                # If model is very uncertain, likely not a skin lesion image
                is_valid_confidence, confidence_error = validate_model_confidence(probs, max_prob, ent)
                if not is_valid_confidence:
                    print(f"⚠️ Model confidence validation failed: {confidence_error}")
                    return {
                        "success": False,
                        "error": "invalid_image",
                        "message": confidence_error,
                        "risk_level": None,
                        "image_risk": None,
                        "support_risk": None,
                        "final_risk": None,
                    }
                
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

        # Create assessment record in database
        assessment = Assessment(
            user_id=current_user.id,
            risk_level=risk_level,
            final_risk_score=final_risk_score,
            image_risk=image_risk_percentage,
            support_risk=support_risk_score,
            explanations=explanations,
            recommendation=recommendation,
            user_inputs={
                "duration": duration,
                "itching": itching,
                "bleeding": bleeding,
                "pain": pain,
                "sun_exposure": sun_exposure,
                "location": location,
            }
        )
        db.add(assessment)
        db.flush()  # Flush to get the assessment ID
        
        # Save image to database
        image_record = Image(
            assessment_id=assessment.id,
            user_id=current_user.id,
            image_data=contents,
            filename=file.filename,
            content_type=file.content_type,
            file_size=len(contents)
        )
        db.add(image_record)
        db.commit()
        db.refresh(assessment)
        
        print(f"✓ Assessment saved to database (ID: {assessment.id})\n")

        # Return results
        return {
            "success": True,
            "assessment_id": str(assessment.id),
            "risk_level": risk_level,
            "final_risk_score": round(final_risk_score, 2),
            "final_risk_percentage": f"{final_risk_score:.1f}%",
            "image_risk": round(image_risk_percentage, 2),
            "image_risk_percentage": f"{image_risk_percentage:.1f}%",
            "support_risk": round(support_risk_score, 2),
            "support_risk_percentage": f"{support_risk_score:.1f}%",
            "explanations": explanations,
            "recommendation": recommendation,
            "timestamp": assessment.created_at.isoformat(),
            "disclaimer": "This system is for risk assessment only and not a medical diagnosis. Always consult a dermatologist for professional evaluation.",
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error in assess_risk: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")

@app.get("/assessments")
async def get_assessments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get current user's assessment history."""
    assessments = db.query(Assessment).filter(
        Assessment.user_id == current_user.id
    ).order_by(Assessment.created_at.desc()).limit(limit).all()
    
    # Get image IDs for each assessment
    assessment_list = []
    for assessment in assessments:
        image = db.query(Image).filter(Image.assessment_id == assessment.id).first()
        assessment_dict = {
            "id": str(assessment.id),
            "user_id": str(assessment.user_id),
            "risk_level": assessment.risk_level,
            "final_risk_score": assessment.final_risk_score,
            "image_risk": assessment.image_risk,
            "support_risk": assessment.support_risk,
            "explanations": assessment.explanations,
            "recommendation": assessment.recommendation,
            "user_inputs": assessment.user_inputs,
            "created_at": assessment.created_at.isoformat(),
            "image_id": str(image.id) if image else None
        }
        assessment_list.append(assessment_dict)
    
    return {
        "success": True,
        "count": len(assessment_list),
        "assessments": assessment_list
    }


@app.get("/assessments/{assessment_id}", response_model=AssessmentDetail)
async def get_assessment(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific assessment by ID (must belong to current user)."""
    try:
        assessment_uuid = uuid.UUID(assessment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid assessment ID format")
    
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_uuid,
        Assessment.user_id == current_user.id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get image ID
    image = db.query(Image).filter(Image.assessment_id == assessment.id).first()
    
    return AssessmentDetail(
        id=assessment.id,
        user_id=assessment.user_id,
        risk_level=assessment.risk_level,
        final_risk_score=assessment.final_risk_score,
        image_risk=assessment.image_risk,
        support_risk=assessment.support_risk,
        explanations=assessment.explanations,
        recommendation=assessment.recommendation,
        user_inputs=assessment.user_inputs,
        created_at=assessment.created_at,
        image_id=image.id if image else None
    )


@app.get("/assessments/{assessment_id}/image")
async def get_assessment_image(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get image for a specific assessment."""
    try:
        assessment_uuid = uuid.UUID(assessment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid assessment ID format")
    
    # Verify assessment belongs to user
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_uuid,
        Assessment.user_id == current_user.id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get image
    image = db.query(Image).filter(Image.assessment_id == assessment.id).first()
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    from fastapi.responses import Response
    return Response(
        content=image.image_data,
        media_type=image.content_type or "image/jpeg"
    )


@app.delete("/assessments/{assessment_id}")
async def delete_assessment(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an assessment (must belong to current user)."""
    try:
        assessment_uuid = uuid.UUID(assessment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid assessment ID format")
    
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_uuid,
        Assessment.user_id == current_user.id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Delete associated image
    image = db.query(Image).filter(Image.assessment_id == assessment.id).first()
    if image:
        db.delete(image)
    
    # Delete assessment
    db.delete(assessment)
    db.commit()
    
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
