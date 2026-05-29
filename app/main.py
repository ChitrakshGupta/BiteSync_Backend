from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.mongo import close_mongo_connection, connect_to_mongo, mongodb


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongo()
    await mongodb.db["users"].create_index("email", unique=True, sparse=True)
    await mongodb.db["users"].create_index("phone", unique=True, sparse=True)
    await mongodb.db["meals"].create_index([("user_id", 1), ("created_at", -1)])
    yield
    await close_mongo_connection()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description=(
        "HealthX backend API with auth, AI meal analysis, calorie tracking, and workout form analysis."
    ),
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    return {"status": "ok", "service": settings.app_name}
