from fastapi import APIRouter, Query, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from src.core.db import get_session
from src.model.user import User
from src.services.user import UserService

auth_router = APIRouter()
users = UserService()
 
@auth_router.post("/signup")
async def signup(user_data: User, session: AsyncSession = Depends(get_session)):
    try:
        new_user = await users.signup(user_data, session)
        return JSONResponse(content={"message": "User created successfully", "user_id": str(new_user.id)}, status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_data: User, session: AsyncSession = Depends(get_session)):
    # Implementation for user login
    pass