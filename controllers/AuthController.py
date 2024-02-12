import jwt
from config import config
from passlib.context import CryptContext
from datetime import datetime, timedelta
import re
from models.User import User
from controllers.UserController import get_user_by_email
from fastapi import HTTPException, status
import uuid

class AuthController:

    def __init__(self, db):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
        self.ALGORITHM = "HS256"
        self.db = db

    def verifyPassword(self,password, password_hash):
        return self.pwd_context.verify(password, password_hash)

    def auth_user(self,email: str, password: str, isLogging: bool):
        client = next(self.db)
        if not isLogging and self.validateFields(email,password):
            try:
                user_search = get_user_by_email(client, email)
                if user_search:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST , detail="User Already Exists"
                    )
                hashed_password = self.get_password_hash(password)
                user_data = {
                    "id": uuid.uuid4().hex,
                    "email": email,
                    "password": hashed_password,
                    "created_at": datetime.now()
                }
                db_user = User(**user_data)
                client.add(db_user)
                client.commit()
                client.refresh(db_user)
                return user_data
            except Exception as e:
                print(e)
                return None
        else:
            user = get_user_by_email(client, email)
            if not user or not self.verifyPassword(password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_405_UNAUTHORIZED, detail="Incorrect password"
                )
            return user    

    def validateFields(self,email,password):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return False
        if not re.match(r"^[a-zA-Z0-9]{8,}$", password):
            return False
        return True

    def get_password_hash(self,password):
        re.match(r"",password)
        return self.pwd_context.hash(password)

    def create_access_token(self,*,data:dict, expires_delta=None):
        data_to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        data_to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            payload=data_to_encode,
            key=config.config().SECRET_KEY,
            algorithm=self.ALGORITHM
        )
        return encode_jwt

    def decode_jwt(self,token):
        return jwt.decode(
            token,
            config.config().SECRET_KEY,
            algorithms=[self.ALGORITHM]
        )