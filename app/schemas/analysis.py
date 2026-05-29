from pydantic import BaseModel, Field


class FoodAnalysisResponse(BaseModel):
    meal_name: str
    description: str
    estimated_weight_grams: float
    calories: float
    protein_grams: float
    carbs_grams: float
    fats_grams: float
    confidence: float = Field(ge=0, le=1)


class FormAnalysisResponse(BaseModel):
    exercise_name: str
    summary: str
    what_is_good: list[str]
    what_is_missing: list[str]
    risk_flags: list[str]
    recommendations: list[str]
    confidence: float = Field(ge=0, le=1)
