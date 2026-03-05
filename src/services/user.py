from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, or_
from src.schemas.user import User as UserSchema, UserLogin
from src.model.user import User as UserModel
from src.utils import generate_password_hash, verify_password 

class UserService:
    async def get_user_by_email_or_username(self, email: str, username: str, session: AsyncSession):
        statement = select(UserModel).where(or_(UserModel.email == email, UserModel.username == username))
        result = await session.execute(statement)
        user = result.scalars().first()
        return user
    
    async def user_exists(self, email: str, username: str, session: AsyncSession):
        user = await self.get_user_by_email_or_username(email, username, session)
        return user is not None
     
    async def signup(self, user_data: UserSchema, session: AsyncSession):
        if await self.user_exists(user_data.email, user_data.username, session):
             raise ValueError("User with this email or username already exists")

        new_user = UserModel(
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=generate_password_hash(user_data.password)
        )
        
        session.add(new_user)
        await session.commit()
        return new_user
    
    async def login(self, user_data: UserLogin, session: AsyncSession):
       statement = select(UserModel).where(UserModel.email == user_data.email)
       result = await session.execute(statement)
       user = result.scalars().first()
       if user and verify_password(user_data.password, user.password):
        return user
       return None