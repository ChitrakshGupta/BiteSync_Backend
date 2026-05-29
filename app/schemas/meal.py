from datetime import datetime

from pydantic import BaseModel, Field


class MealCreateManualRequest(BaseModel):
    meal_name: str = Field(min_length=2, max_length=100)
    weight_grams: float = Field(gt=0)
    calories: float = Field(gt=0)
    protein_grams: float | None = Field(default=0, ge=0)
    carbs_grams: float | None = Field(default=0, ge=0)
    fats_grams: float | None = Field(default=0, ge=0)


class MealResponse(BaseModel):
    id: str
    user_id: str
    source: str
    meal_name: str
    weight_grams: float | None = None
    calories: float
    protein_grams: float | None = None
    carbs_grams: float | None = None
    fats_grams: float | None = None
    description: str | None = None
    created_at: datetime


class DailyCalorieSummaryResponse(BaseModel):
    date: str
    total_meals: int
    total_calories: float
    total_protein_grams: float
    total_carbs_grams: float
    total_fats_grams: float
    meals: list[MealResponse]
