from datetime import date, datetime, time, timedelta, timezone

from bson import ObjectId

from app.db.mongo import mongodb
from app.schemas.meal import MealCreateManualRequest
from app.utils.common import utc_now


class MealService:
    @staticmethod
    async def add_manual_meal(user_id: str, payload: MealCreateManualRequest) -> dict:
        meal_doc = {
            "user_id": ObjectId(user_id),
            "source": "manual",
            "meal_name": payload.meal_name,
            "weight_grams": payload.weight_grams,
            "calories": payload.calories,
            "protein_grams": payload.protein_grams or 0,
            "carbs_grams": payload.carbs_grams or 0,
            "fats_grams": payload.fats_grams or 0,
            "description": f"Manual meal entry for {payload.meal_name}",
            "created_at": utc_now(),
        }
        result = await mongodb.db["meals"].insert_one(meal_doc)
        meal_doc["_id"] = result.inserted_id
        return meal_doc

    @staticmethod
    async def add_ai_meal(user_id: str, ai_data: dict) -> dict:
        meal_doc = {
            "user_id": ObjectId(user_id),
            "source": "ai_image",
            "meal_name": ai_data.get("meal_name", "Unknown meal"),
            "weight_grams": float(ai_data.get("estimated_weight_grams", 0) or 0),
            "calories": float(ai_data.get("calories", 0) or 0),
            "protein_grams": float(ai_data.get("protein_grams", 0) or 0),
            "carbs_grams": float(ai_data.get("carbs_grams", 0) or 0),
            "fats_grams": float(ai_data.get("fats_grams", 0) or 0),
            "description": ai_data.get("description", ""),
            "created_at": utc_now(),
        }
        result = await mongodb.db["meals"].insert_one(meal_doc)
        meal_doc["_id"] = result.inserted_id
        return meal_doc

    @staticmethod
    async def get_daily_summary(user_id: str, summary_date: date | None = None) -> dict:
        target_date = summary_date or datetime.now(timezone.utc).date()
        start_dt = datetime.combine(target_date, time.min, tzinfo=timezone.utc)
        end_dt = start_dt + timedelta(days=1)

        query = {
            "user_id": ObjectId(user_id),
            "created_at": {
                "$gte": start_dt,
                "$lt": end_dt,
            },
        }

        cursor = mongodb.db["meals"].find(query).sort("created_at", -1)
        meals = await cursor.to_list(length=500)

        total_calories = sum(float(item.get("calories", 0) or 0) for item in meals)
        total_protein = sum(float(item.get("protein_grams", 0) or 0) for item in meals)
        total_carbs = sum(float(item.get("carbs_grams", 0) or 0) for item in meals)
        total_fats = sum(float(item.get("fats_grams", 0) or 0) for item in meals)

        return {
            "date": target_date.isoformat(),
            "total_meals": len(meals),
            "total_calories": round(total_calories, 2),
            "total_protein_grams": round(total_protein, 2),
            "total_carbs_grams": round(total_carbs, 2),
            "total_fats_grams": round(total_fats, 2),
            "meals": meals,
        }
