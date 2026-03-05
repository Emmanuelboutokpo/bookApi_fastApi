from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from src.api.dependencies import AccessTokenBearer
from src.core.db import get_session
from src.model.user import User
from src.services.user import UserService
from src.utils import generateAccessToken, generateRefreshToken

auth_router = APIRouter()
users = UserService()
 
@auth_router.post("/signup")
async def signup(user_data: User, session: AsyncSession = Depends(get_session)):
    try:
        new_user = await users.signup(user_data, session)
        return JSONResponse(content={"message": "User created successfully", "user_id": str(new_user.id)}, status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    

@auth_router.post("/login")
async def login(login_data: User, session: AsyncSession = Depends(get_session)):
    user = await users.login(login_data, session)
    
    if not user:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe incorrect")

    access_token = generateAccessToken(user_data={"sub": str(user.id), "email": user.email})
    refresh_token = generateRefreshToken(user_data={"sub": str(user.id), "email": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "email": user.email,
            "username": user.username
        }
    }