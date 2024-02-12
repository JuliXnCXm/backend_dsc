from sqlalchemy.orm import Session
from models.User import User as user_model
from fastapi import status,HTTPException, UploadFile
import shutil
import os

UPLOAD_FOLDER = "storage"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_user(db: Session, user_id: str):
    return db.query(user_model).filter(user_model.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(user_model).filter(user_model.email == email).first()

def save_image(image: UploadFile, filename):
    image_path = os.path.join(UPLOAD_FOLDER, filename+"."+image.filename.split('.')[-1])
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return image_path
def get_users(db: Session, skip: int = 0, limit: int = 100, roleUser:str = None):
    
    return db.query(user_model).offset(skip).limit(limit).all()
    if roleUser == "ADMIN":
        return db.query(user_model).offset(skip).limit(limit).all()
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient permissions"
            )