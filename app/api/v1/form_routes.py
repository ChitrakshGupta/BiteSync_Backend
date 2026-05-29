from fastapi import APIRouter, Depends, File, UploadFile

from app.api.deps import current_user
from app.schemas.analysis import FormAnalysisResponse
from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/form", tags=["Workout Form Analysis"])


@router.post("/analyze-video", response_model=FormAnalysisResponse)
async def analyze_workout_video(
    video: UploadFile = File(..., description="Workout video clip, ideally <= 30 seconds"),
    _: dict = Depends(current_user),
) -> FormAnalysisResponse:
    video_bytes = await video.read()
    result = await GeminiService.analyze_workout_video(
        video_bytes=video_bytes,
        mime_type=video.content_type or "video/mp4",
    )
    return FormAnalysisResponse(**result)
