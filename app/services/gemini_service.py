import json
from typing import Any

import google.generativeai as genai
from fastapi import HTTPException

from app.core.config import settings


genai.configure(api_key=settings.gemini_api_key)


class GeminiService:
    @staticmethod
    def _get_model() -> Any:
        return genai.GenerativeModel(settings.gemini_model)

    @staticmethod
    def _parse_json_text(text: str) -> dict:
        cleaned = text.strip().replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=502, detail="Failed to parse AI response") from exc

    @staticmethod
    async def analyze_food_image(image_bytes: bytes, mime_type: str) -> dict:
        prompt = (
            "You are a nutrition expert. Analyze the food image and return STRICT JSON with keys: "
            "meal_name (string), description (string), estimated_weight_grams (number), calories (number), "
            "protein_grams (number), carbs_grams (number), fats_grams (number), confidence (0-1 number)."
        )

        try:
            model = GeminiService._get_model()
            response = await model.generate_content_async(
                [
                    prompt,
                    {
                        "mime_type": mime_type,
                        "data": image_bytes,
                    },
                ]
            )
            return GeminiService._parse_json_text(response.text)
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Food analysis failed: {exc}") from exc

    @staticmethod
    async def analyze_workout_video(video_bytes: bytes, mime_type: str) -> dict:
        prompt = (
            "You are a fitness coach. Analyze this short workout clip and return STRICT JSON with keys: "
            "exercise_name (string), summary (string), what_is_good (array of strings), "
            "what_is_missing (array of strings), risk_flags (array of strings), "
            "recommendations (array of strings), confidence (0-1 number)."
        )

        try:
            model = GeminiService._get_model()
            response = await model.generate_content_async(
                [
                    prompt,
                    {
                        "mime_type": mime_type,
                        "data": video_bytes,
                    },
                ]
            )
            return GeminiService._parse_json_text(response.text)
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Video form analysis failed: {exc}") from exc
