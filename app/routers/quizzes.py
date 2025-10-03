from fastapi import APIRouter, Depends, status
from app.schemas.user import UserResponse
from app.services.quiz import QuizService
from app.utils.deps import get_current_user, get_quiz_service

from app.schemas.quiz import (
    QuestionRequest,
    QuizCreateRequest,
    QuizFullResponse,
    QuizListResponse,
    QuizResponse,
    QuizUpdateRequest,
)


router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


@router.post("/", response_model=QuizFullResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz(
    data: QuizCreateRequest,
    current_user: UserResponse = Depends(get_current_user),
    service: QuizService = Depends(get_quiz_service),
):
    return await service.create_quiz(data, user_id=current_user.id)


@router.get("/{quiz_id}", response_model=QuizFullResponse)
async def get_quiz(
    quiz_id: int,
    service: QuizService = Depends(get_quiz_service),
):
    return await service.get_quiz_or_404(quiz_id)


@router.get("/company/{company_id}", response_model=QuizListResponse)
async def get_company_quizzes(
    company_id: int,
    skip: int = 0,
    limit: int = 10,
    service: QuizService = Depends(get_quiz_service),
):
    return await service.get_company_quizzes(company_id, skip, limit)


@router.put("/{quiz_id}", response_model=QuizFullResponse)
async def update_quiz(
    quiz_id: int,
    data: QuizUpdateRequest,
    current_user: UserResponse = Depends(get_current_user),
    service: QuizService = Depends(get_quiz_service),
):
    return await service.update_quiz(quiz_id, data, user_id=current_user.id)


@router.delete("/{quiz_id}", response_model=QuizResponse)
async def update_quiz(
    quiz_id: int,
    current_user: UserResponse = Depends(get_current_user),
    service: QuizService = Depends(get_quiz_service),
):
    return await service.delete_quiz(quiz_id, user_id=current_user.id)


@router.post("/{quiz_id}/questions", response_model=QuizFullResponse)
async def add_question(
    quiz_id: int,
    data: QuestionRequest,
    current_user: UserResponse = Depends(get_current_user),
    service: QuizService = Depends(get_quiz_service),
):
    return await service.add_question(quiz_id, data, user_id=current_user.id)


@router.put("/questions/{question_id}", response_model=QuizFullResponse)
async def update_question(
    question_id: int,
    data: QuestionRequest,
    current_user: UserResponse = Depends(get_current_user),
    service: QuizService = Depends(get_quiz_service),
):
    return await service.update_question(question_id, data, user_id=current_user.id)


@router.delete("/questions/{question_id}", response_model=QuizFullResponse)
async def delete_question(
    question_id: int,
    current_user: UserResponse = Depends(get_current_user),
    service: QuizService = Depends(get_quiz_service),
):
    return await service.delete_question(question_id, user_id=current_user.id)
