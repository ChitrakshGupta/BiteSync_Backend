from bson import ObjectId
from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.core.config import settings
from app.db.mongo import mongodb
from app.schemas.auth import LoginRequest, SignupRequest
from app.utils.common import utc_now
from app.utils.security import create_access_token, hash_password, verify_password


class AuthService:
    @staticmethod
    async def signup(payload: SignupRequest) -> dict:
        if not payload.email and not payload.phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either email or phone is required",
            )

        users = mongodb.db["users"]

        if payload.email:
            existing_by_email = await users.find_one({"email": payload.email.lower()})
            if existing_by_email:
                raise HTTPException(status_code=409, detail="Email already registered")

        if payload.phone:
            existing_by_phone = await users.find_one({"phone": payload.phone})
            if existing_by_phone:
                raise HTTPException(status_code=409, detail="Phone already registered")

        user_doc = {
            "full_name": payload.full_name,
            "email": payload.email.lower() if payload.email else None,
            "phone": payload.phone,
            "password_hash": hash_password(payload.password),
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "last_login_at": None,
            "active": True,
        }
        result = await users.insert_one(user_doc)
        user_id = str(result.inserted_id)
        token = create_access_token(subject=user_id)
        return {"access_token": token, "user_id": user_id}

    @staticmethod
    async def login(payload: LoginRequest) -> dict:
        users = mongodb.db["users"]
        identifier = payload.identifier.strip()

        if "@" in identifier:
            user = await users.find_one({"email": identifier.lower()})
        else:
            user = await users.find_one({"phone": identifier})

        if not user or not verify_password(payload.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        await users.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "last_login_at": utc_now(),
                    "updated_at": utc_now(),
                    "last_device": {
                        "device_type": payload.device_type,
                        "device_id": payload.device_id,
                    },
                }
            },
        )

        user_id = str(user["_id"])
        token = create_access_token(subject=user_id)
        return {"access_token": token, "user_id": user_id}

    @staticmethod
    async def get_current_user(token: str) -> dict:
        unauthorized = HTTPException(status_code=401, detail="Could not validate credentials")
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            user_id: str | None = payload.get("sub")
            if not user_id:
                raise unauthorized
        except JWTError as exc:
            raise unauthorized from exc

        user = await mongodb.db["users"].find_one({"_id": ObjectId(user_id), "active": True})
        if not user:
            raise unauthorized
        return user
