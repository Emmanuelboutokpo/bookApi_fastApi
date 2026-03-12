from typing import Any
from typing import List
from src.model.user import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils import decode_access_token
from fastapi import Depends, Request
from src.core.redis import token_in_blacklist
from src.core.db import get_session
from src.services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from src.errors import InvalidToken, AccessTokenRequired, RefreshTokenRequired, InsufficientPermission

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None: 
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)

        if not self.valide_token(token):
            raise InvalidToken()
        
        if await token_in_blacklist(token_data.get('jti')):
            print(f"Token with jti: {token_data.get('jti')} is in blacklist")
            raise InvalidToken()
            
        self.verify_token_data(token_data)  
        return token_data
    
    def valide_token(self, token: str) -> bool:
         token_data = decode_access_token(token)
         return token_data is not None

    def verify_token_data(self, token_data: dict) -> bool:
        raise NotImplementedError("Subclasses must implement this method")
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get('refresh'):
                raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get('refresh'):
                raise RefreshTokenRequired()

async def get_current_user( token_details: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    user_email = token_details["user"]["email"]
    user = await user_service.get_user_by_email_or_username(user_email, None, session)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True

        raise InsufficientPermission()