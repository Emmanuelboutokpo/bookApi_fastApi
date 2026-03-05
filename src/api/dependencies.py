from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils import decode_access_token
from fastapi import HTTPException, status,Request

class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None: 
        creds = await super().__call__(request)
        
        if creds:
            token = creds.credentials
            token_data = decode_access_token(token)

            if not token_data:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or expired token"
                )

            if token_data.get('refresh'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Please provide an access token, not a refresh token"
                )
            
            return token_data
        
        return None  
    def valide_token(self, token: str) -> bool:
         token_data = decode_access_token(token)
         return True if token_data is not None else False