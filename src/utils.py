import uuid
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from datetime import datetime, timedelta
import jwt
from src.config import settings
from fastapi import HTTPException

def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def generateAccessToken(user_data: dict, expires_delta: timedelta=None, refresh: bool= False) -> str:
    payload = {
        'user':user_data,
        'exp': datetime.now() + (expires_delta if expires_delta is not None else timedelta(minutes=60)),
        'jti': str(uuid.uuid4()),
        'refresh' : refresh
    }

    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")