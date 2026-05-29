from datetime import date

from fastapi import APIRouter, Depends, File, Query, UploadFile

from app.api.deps import current_user
from app.models.serializers import serialize_meal
from app.schemas.analysis import FoodAnalysisResponse
from app.schemas.meal import (
    DailyCalorieSummaryResponse,
    MealCreateManualRequest,
    MealResponse,
)
from app.services.gemini_service import GeminiService
from app.services.meal_service import MealService

router = APIRouter(prefix="/meals", tags=["Meals"])


@router.post("/manual", response_model=MealResponse)
async def add_manual_meal(payload: MealCreateManualRequest, user: dict = Depends(current_user)) -> MealResponse:
    meal = await MealService.add_manual_meal(str(user["_id"]), payload)
    return MealResponse(**serialize_meal(meal))


@router.post("/analyze-image", response_model=FoodAnalysisResponse)
async def analyze_food_image(
    image: UploadFile = File(..., description="Food image file (jpg/png/webp)"),
    user: dict = Depends(current_user),
) -> FoodAnalysisResponse:
    image_bytes = await image.read()
    ai_result = await GeminiService.analyze_food_image(
        image_bytes=image_bytes,
        mime_type=image.content_type or "image/jpeg",
    )
    await MealService.add_ai_meal(str(user["_id"]), ai_result)
    return FoodAnalysisResponse(**ai_result)


@router.get("/summary", response_model=DailyCalorieSummaryResponse)
async def get_daily_summary(
    date_value: date | None = Query(default=None, alias="date", description="YYYY-MM-DD"),
    user: dict = Depends(current_user),
) -> DailyCalorieSummaryResponse:
    summary = await MealService.get_daily_summary(str(user["_id"]), date_value)
    summary["meals"] = [MealResponse(**serialize_meal(item)) for item in summary["meals"]]
    return DailyCalorieSummaryResponse(**summary)
