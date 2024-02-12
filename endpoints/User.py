from schemas import User as user_models
from fastapi import APIRouter, status,HTTPException, Request, UploadFile, File
from controllers.UserController import get_user , get_users, save_image, UPLOAD_FOLDER
from connection import ConnDb
from controllers.AuthController import AuthController
from controllers.TokenController import TokenController
import re
from config.config import config
from datetime import timedelta
from fastapi.encoders import jsonable_encoder
import os

router = APIRouter(
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    path="/user",
    tags=["User"],
    summary="User",
    description="get user information",
    response_description="User information",
    status_code=status.HTTP_200_OK)
def return_user(req: Request) -> dict:
    """Get a user by their ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        user_models: The requested user, or None if not found.
    """
    db = next(ConnDb.Connection().get_db())
    user_id = TokenController(req).decodeToken()
    print(user_id)
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user" : {
        "id" : db_user.id,
        "email": db_user.email,
        "name": db_user.name,
        "lastname": db_user.lastname,
        "role": db_user.role,
        "created_at": db_user.created_at,
        "is_active": db_user.is_active,
        "picture_url": db_user.picture_url
    }}

@router.get(
    path="/users",
    tags=["User"],
    summary="User",
    description="get user information",
    response_description="User information",
    status_code=status.HTTP_200_OK)
def return_users(req: Request):
    """Get a user by their ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        user_models: The requested user, or None if not found.
    """
    db = ConnDb.Connection().get_db()
    users = get_users(db=db)
    return users

@router.post(
    path="/user/user_image",
    tags=["User"],
    summary="User",
    description="update user image",
    response_description="User information",
    status_code=status.HTTP_200_OK)
def update_user_image(req: Request, image: UploadFile = File(...)):
    try:
        db = next(ConnDb.Connection().get_db())
        user_id = TokenController(req).decodeToken()
        user = get_user(db,user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        image_path = save_image(image, user_id)
        update_user({
            "picture_url" : config.API_URL+image_path},
            req)
        return {"message": "Imagen actualizada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.put(
    path="/user",
    tags=["User"],
    summary="User profile updated",
    description="update user information",
    response_description="Update User information",
    status_code=status.HTTP_200_OK)
def update_user(user: dict , req: Request):
    db = next(ConnDb.Connection().get_db())
    user_id = TokenController(req).decodeToken()
    try:
        auth_handler = AuthController(db)
        db_user = get_user(db=db, user_id=user_id)
        if db_user:
            for key, value in user.items():
                if key == "email":
                    if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
                        setattr(db_user, key, value)
                    else:
                        raise HTTPException(status_code=404, detail="Email No valido")
                if key == "password":
                    if re.match(r"^[a-zA-Z0-9]{8,}$", value):
                        hashed_password = auth_handler.get_password_hash(value)
                        setattr(db_user, key, hashed_password)
                    else:
                        raise HTTPException(status_code=404, detail="Password No valido")
                setattr(db_user, key, value)
            db.commit()
            access_token_expires = timedelta(minutes=60 * 24 * 7)
            access_token = auth_handler.create_access_token(
                data={"sub": db_user.id}, expires_delta=access_token_expires
            )
            token = jsonable_encoder(access_token)
            return {"token":token}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="User not found")