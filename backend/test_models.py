"""
Test script to verify models are loaded correctly
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

print("="*60)
print("Testing Model Loading")
print("="*60)

# Check if model files exist
print("\n1. Checking model files...")
cnn_path = MODEL_DIR / "risk_cnn_densenet201.h5"
rf_path = MODEL_DIR / "risk_random_forest.joblib"
metadata_path = MODEL_DIR / "risk_metadata.json"

files_exist = True
if cnn_path.exists():
    print(f"   ✓ {cnn_path.name} found")
else:
    print(f"   ✗ {cnn_path.name} NOT FOUND")
    files_exist = False

if rf_path.exists():
    print(f"   ✓ {rf_path.name} found")
else:
    print(f"   ✗ {rf_path.name} NOT FOUND")
    files_exist = False

if metadata_path.exists():
    print(f"   ✓ {metadata_path.name} found")
else:
    print(f"   ⚠ {metadata_path.name} not found (optional)")

if not files_exist:
    print("\n❌ Model files are missing! Please add them to backend/models/")
    sys.exit(1)

# Try loading models
print("\n2. Attempting to load models...")
try:
    from tensorflow import keras
    print("   ✓ TensorFlow imported")
    
    cnn_model = keras.models.load_model(cnn_path)
    print(f"   ✓ CNN model loaded successfully")
    print(f"      Input shape: {cnn_model.input_shape}")
    print(f"      Output shape: {cnn_model.output_shape}")
except Exception as e:
    print(f"   ✗ Failed to load CNN model: {e}")
    sys.exit(1)

try:
    import joblib
    print("   ✓ Joblib imported")
    
    rf_model = joblib.load(rf_path)
    print(f"   ✓ Random Forest model loaded successfully")
    
    if hasattr(rf_model, 'classes_'):
        print(f"      Classes: {rf_model.classes_}")
    if hasattr(rf_model, 'n_estimators'):
        print(f"      Number of trees: {rf_model.n_estimators}")
except Exception as e:
    print(f"   ✗ Failed to load Random Forest model: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("✅ All models loaded successfully!")
print("="*60)
print("\nYou can now start the backend server with: python main.py")

