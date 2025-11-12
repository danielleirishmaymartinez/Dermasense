from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os, shutil

app = FastAPI(
    title="DermaSense API",
    description="Backend for skin lesion analysis prototype",
    version="1.0.0",
)

# Allow your Vue frontend to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later: restrict to http://localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder for uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/")
def root():
    return {"message": "DermaSense API is running"}

@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    age: str = Form(None),
    sex: str = Form(None),
    site: str = Form(None),
):
    """Temporary endpoint for testing."""
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = {
        "label": "Basal Cell Carcinoma (BCC)",
        "confidence": "86.7%",
        "description": (
            "This lesion shows visual features commonly associated with BCC. "
            "Please consult a dermatologist for confirmation."
        ),
        "image_url": f"/uploads/{file.filename}",
    }
    return JSONResponse(content=result)
