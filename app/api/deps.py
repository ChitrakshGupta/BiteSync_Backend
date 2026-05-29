from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.auth_service import AuthService

bearer_scheme = HTTPBearer(auto_error=True)


async def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    return await AuthService.get_current_user(credentials.credentials)
