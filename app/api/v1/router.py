from fastapi import APIRouter

from app.api.v1.auth_routes import router as auth_router
from app.api.v1.form_routes import router as form_router
from app.api.v1.meal_routes import router as meal_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(meal_router)
api_router.include_router(form_router)
