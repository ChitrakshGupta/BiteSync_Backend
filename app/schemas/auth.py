from pydantic import BaseModel, EmailStr, Field, field_validator


class SignupRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr | None = None
    phone: str | None = None
    password: str = Field(min_length=6, max_length=128)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str | None) -> str | None:
        if value and not value.strip().replace("+", "", 1).isdigit():
            raise ValueError("Phone number must contain only digits and optional leading +")
        return value


class LoginRequest(BaseModel):
    identifier: str = Field(
        description="Email or phone number. Enables dynamic login for mobile apps and web apps"
    )
    password: str
    device_type: str | None = Field(default=None, description="android | ios | web")
    device_id: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str


class UserProfileResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr | None = None
    phone: str | None = None
