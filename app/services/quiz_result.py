from sqlalchemy.ext.asyncio import AsyncSession

from app.db.redis import RedisService
from app.repositories.quiz import (
    QuizResultRepository,
)
from app.schemas.quiz import (
    AverageScoreResponse,
    CheckQuiz,
    QuizResultResponse,
)
from app.services.quiz import QuizService
from app.services.quiz_result_redis import QuizResultRedisService


class QuizResultService:

    def __init__(self, db: AsyncSession, redis: RedisService):
        self.quiz_result_repo = QuizResultRepository(db)
        self.quiz_service = QuizService(db)
        self.quiz_redis_service = QuizResultRedisService(db, redis)

    async def check_quiz(self, data: CheckQuiz, user_id: int) -> QuizResultResponse:
        quiz = await self.quiz_service.get_quiz_or_404(data.quiz_id)

        correct_answers = 0
        score = 0

        for question in quiz.questions:
            question_answer = next(
                (qa for qa in data.question_answers if qa.question_id == question.id),
                None,
            )

            if question_answer is None:
                continue

            correct_option_ids = {
                ao.id for ao in question.answer_options if ao.is_correct
            }
            selected_option_ids = set(question_answer.answers)

            if selected_option_ids == correct_option_ids:
                correct_answers += 1

        if len(quiz.questions) > 0:
            score = (correct_answers / len(quiz.questions)) * 100

        await self.quiz_result_repo.add_one(
            {
                "quiz_id": data.quiz_id,
                "user_id": user_id,
                "company_id": quiz.company_id,
                "correct_answers": correct_answers,
                "total_questions": len(quiz.questions),
            }
        )

        question_answers_dict = [
            {"question_id": qa.question_id, "answers": qa.answers}
            for qa in data.question_answers
        ]

        correct_answers_map = {
            q.id: [ao.id for ao in q.answer_options if ao.is_correct]
            for q in quiz.questions
        }

        await self.quiz_redis_service.save_user_answers(
            user_id=user_id,
            company_id=quiz.company_id,
            quiz_id=data.quiz_id,
            question_answers=question_answers_dict,
            correct_answers_map=correct_answers_map,
        )

        return QuizResultResponse(
            quiz_id=data.quiz_id,
            score=score,
            total_questions=len(quiz.questions),
            correct_answers=correct_answers,
        )

    async def get_average_score_by_user(self, user_id: int) -> AverageScoreResponse:
        quiz_results = await self.quiz_result_repo.find_all(user_id=user_id)

        total_questions = 0
        correct_answers = 0
        score = 0

        for quiz_result in quiz_results:
            total_questions += quiz_result.total_questions
            correct_answers += quiz_result.correct_answers

        if total_questions > 0:
            score = (correct_answers / total_questions) * 100

        return AverageScoreResponse(
            total_questions=total_questions,
            correct_answers=correct_answers,
            score=score,
        )

    async def get_average_score_by_user_and_company(
        self, user_id: int, company_id: int
    ) -> AverageScoreResponse:
        quiz_results = await self.quiz_result_repo.find_all(
            user_id=user_id, company_id=company_id
        )

        total_questions = 0
        correct_answers = 0
        score = 0

        for quiz_result in quiz_results:
            total_questions += quiz_result.total_questions
            correct_answers += quiz_result.correct_answers

        if total_questions > 0:
            score = (correct_answers / total_questions) * 100

        return AverageScoreResponse(
            total_questions=total_questions,
            correct_answers=correct_answers,
            score=score,
        )
