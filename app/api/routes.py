from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.api.schemas import PredictionResponse
from app.inference.predict import predict

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

UPLOAD_DIR = PROJECT_ROOT / "uploads"

UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/")
def home():

    return {
        "message": "Brain Tumor Detection API is Running"
    }


@router.post(
    "/predict",
    response_model=PredictionResponse
)
async def predict_image(
    file: UploadFile = File(...)
):

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image."
        )

    extension = Path(file.filename).suffix

    filename = f"{uuid.uuid4()}{extension}"

    filepath = UPLOAD_DIR / filename

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = predict(filepath)

    return PredictionResponse(**result)