import base64
from fastapi import APIRouter, status,Depends,Response,HTTPException
from fastapi.security import HTTPBasic
from controllers.BasicAuth import BasicAuth
from schemas.User import UserBase
from datetime import timedelta
from fastapi.encoders import jsonable_encoder
from controllers.AuthController import AuthController
from connection import ConnDb


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"

router = APIRouter(
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

security = HTTPBasic()
basic_auth = BasicAuth(auto_error=False)

@router.post(
    path="/auth/login",
    tags=["Auth"],
    summary="Login",
    description="Login",
    response_description="Login",
    status_code=status.HTTP_200_OK)
def login(user: UserBase):
    """
    Login to the system.

    Args:
        auth (HTTPBasic): HTTP Basic Auth credentials

    Returns:
        JSON Web Token: Access token to access protected resources

    Raises:
        HTTPException: If the email or password is incorrect
    """
    
    db = ConnDb.Connection().get_db()

    if not user:
        response = Response(
            headers={"WWW-Authenticate": "Basic"}, status_code=status.HTTP_401_UNAUTHORIZED
        )
        return response
    try:
        auth_handler = AuthController(db)
        email, password = user.email, user.password
        user_data = auth_handler.auth_user(email, password, True)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_handler.create_access_token(
            data={"sub": user_data.id}, expires_delta=access_token_expires
        )
        token = jsonable_encoder(access_token)
        return {"token":token}
    except Exception as e:
        response = Response(
            headers={"WWW-Authenticate": "Basic"}, status_code=status.HTTP_401_UNAUTHORIZED
        )
        return response
@router.post(
    path="/auth/register",
    tags=["Auth"],
    summary="Register",
    description="Register a user",
    response_description="Register",
    status_code=status.HTTP_201_CREATED)
def register(user:UserBase):
    """
    Register a new user.

    Args:
        auth (HTTPBasic): HTTP Basic Auth credentials

    Returns:
        JSON Web Token: Access token to access protected resources

    Raises:
        HTTPException: If the email or password is incorrect
    """
    
    db = ConnDb.Connection().get_db()
    try:
        auth_handler = AuthController(db)
        email, password = user.email, user.password
        user_data = auth_handler.auth_user(email, password, False)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="There was an error creating the user"
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_handler.create_access_token(
            data={"sub": user_data["id"]}, expires_delta=access_token_expires
        )
        token = jsonable_encoder(access_token)
        
        return {"token": token}
    except Exception as e:
        print(e)
        response = Response(
            headers={"WWW-Authenticate": "Basic"}, 
            status_code=status.HTTP_401_UNAUTHORIZED, 
            content="There was an error creating the user"
        )
        return response
