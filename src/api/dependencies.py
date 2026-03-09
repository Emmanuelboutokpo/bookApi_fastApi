from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils import decode_access_token
from fastapi import HTTPException, status,Request
from src.core.redis import token_in_blacklist

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None: 
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)

        if not self.valide_token(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )
        
        if await token_in_blacklist(token_data.get('jti')):
            print(f"Token with jti: {token_data.get('jti')} is in blacklist")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token has been revoked"
            )
            
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
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Please provide an access token, not a refresh token"
                )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get('refresh'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Please provide a refresh token, not an access token"
                )






