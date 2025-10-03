from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, StreamingResponse
from app.models.user import User
from app.services.quiz_export_service import QuizExportService
from app.utils.deps import get_current_user, get_quiz_export_service

router = APIRouter(prefix="/export", tags=["Export Data"])


@router.get("/quiz")
async def export_quiz_data(
    format: str = Query("json", enum=["json", "csv"]),
    user_id: Optional[int] = None,
    quiz_id: Optional[int] = None,
    export_service: QuizExportService = Depends(get_quiz_export_service),
    current_user: User = Depends(get_current_user),
):

    if format == "json":
        data = await export_service.export_as_json(current_user, user_id, quiz_id)
        return JSONResponse(content=data)

    csv_data = await export_service.export_as_csv(current_user, user_id, quiz_id)
    return StreamingResponse(
        csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=quiz_export.csv"},
    )
