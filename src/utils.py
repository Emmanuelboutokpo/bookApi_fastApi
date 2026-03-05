from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from datetime import datetime, timedelta
import jwt
from src.config import settings

def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def generateAccessToken(user_data: dict, expires_delta: timedelta=None) -> str:
    payload = {}
    payload.update(user_data)

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.access_token_expire_minutes)
    payload.update({"exp": expire})

    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token

def generateRefreshToken(user_data: dict, expires_delta: timedelta=None) -> str:
    payload = {}
    payload.update(user_data)

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=settings.refresh_token_expire_days)
    payload.update({"exp": expire})

    token = jwt.encode(payload, settings.refresh_token_secret_key, algorithm=settings.algorithm)
    return token

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")