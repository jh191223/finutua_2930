from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserPhoto
from app.auth import get_current_user
from app.services.body_analysis import analyze_body_from_image
import boto3
from app.config import settings
import uuid

router = APIRouter()

s3_client = boto3.client('s3', region_name=settings.AWS_REGION)

@router.post("/upload")
async def upload_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 파일 확장자 검증
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Only JPG/PNG files allowed")
    
    # S3에 업로드
    file_key = f"photos/{current_user.id}/{uuid.uuid4()}.jpg"
    s3_client.upload_fileobj(file.file, settings.S3_BUCKET, file_key)
    photo_url = f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{file_key}"
    
    # 신체 측정 분석 (MediaPipe)
    measurements = analyze_body_from_image(file.file)
    
    # DB에 저장
    new_photo = UserPhoto(
        user_id=current_user.id,
        photo_url=photo_url,
        measurements=measurements,
        is_primary=True
    )
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    
    return {
        "photo_id": new_photo.id,
        "photo_url": photo_url,
        "measurements": measurements
    }

@router.get("/list")
def list_photos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    photos = db.query(UserPhoto).filter(UserPhoto.user_id == current_user.id).all()
