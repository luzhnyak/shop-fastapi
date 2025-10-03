from fastapi import APIRouter, Depends, status
from app.schemas.user import UserResponse
from app.services.quiz_result import QuizResultService
from app.utils.deps import get_current_user, get_quiz_result_service

from app.schemas.quiz import (
    AverageScoreResponse,
    CheckQuiz,
    QuizResultResponse,
)


router = APIRouter(prefix="/quiz_results", tags=["Quiz Results"])


@router.post(
    "/", response_model=QuizResultResponse, status_code=status.HTTP_201_CREATED
)
async def check_quiz(
    data: CheckQuiz,
    service: QuizResultService = Depends(get_quiz_result_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return await service.check_quiz(data, user_id=current_user.id)


@router.get("average-score/user/{user_id}", response_model=AverageScoreResponse)
async def get_average_score_by_user(
    user_id: int,
    service: QuizResultService = Depends(get_quiz_result_service),
):
    return await service.get_average_score_by_user(user_id)


@router.get(
    "average-score/user/{user_id}/company/{company_id}",
    response_model=AverageScoreResponse,
)
async def get_average_score_by_user_and_company(
    company_id: int,
    user_id: int,
    service: QuizResultService = Depends(get_quiz_result_service),
):
    return await service.get_average_score_by_user_and_company(company_id, user_id)
