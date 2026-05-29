from fastapi import APIRouter, Depends

from app.api.deps import current_user
from app.models.serializers import serialize_user
from app.schemas.auth import (
    LoginRequest,
    SignupRequest,
    TokenResponse,
    UserProfileResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=TokenResponse)
async def signup(payload: SignupRequest) -> TokenResponse:
    result = await AuthService.signup(payload)
    return TokenResponse(access_token=result["access_token"], user_id=result["user_id"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    result = await AuthService.login(payload)
    return TokenResponse(access_token=result["access_token"], user_id=result["user_id"])


@router.get("/me", response_model=UserProfileResponse)
async def me(user: dict = Depends(current_user)) -> UserProfileResponse:
    return UserProfileResponse(**serialize_user(user))
