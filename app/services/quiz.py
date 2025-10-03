from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenException, NotFoundException
from app.models.membership import MembershipStatus
from app.repositories.company import CompanyRepository
from app.repositories.membership import MembershipRepository
from app.repositories.quiz import (
    AnswerOptionRepository,
    QuestionRepository,
    QuizRepository,
    QuizResultRepository,
)
from app.schemas.quiz import (
    AnswerOptionRequest,
    CheckQuiz,
    QuestionRequest,
    QuizCreateRequest,
    QuizListResponse,
    QuizFullResponse,
    QuizResponse,
    QuizResultResponse,
    QuizUpdateRequest,
)


class QuizService:

    def __init__(self, db: AsyncSession):
        self.quiz_repo = QuizRepository(db)
        self.question_repo = QuestionRepository(db)
        self.answer_repo = AnswerOptionRepository(db)
        self.quiz_result_repo = QuizResultRepository(db)
        self.db = db

    async def create_quiz(
        self, data: QuizCreateRequest, user_id: int
    ) -> QuizFullResponse:
        await self._check_company_permission(data.company_id, user_id)

        quiz_dict = data.model_dump(exclude={"questions"})
        quiz = await self.quiz_repo.add_one(quiz_dict)

        for q in data.questions:
            question = await self.question_repo.add_one(
                {"title": q.title, "quiz_id": quiz["id"]}
            )

            answer_options_data = self._dump_answer_options(
                q.answer_options, question["id"]
            )

            await self.answer_repo.add_many(answer_options_data)

        full_quiz = await self.quiz_repo.get_full_quiz(quiz["id"])
        return QuizFullResponse.model_validate(full_quiz)

    async def get_quiz_by_id(self, quiz_id: int) -> QuizFullResponse:
        quiz = await self.quiz_repo.get_full_quiz(quiz_id)
        if not quiz:
            return None
        return QuizFullResponse.model_validate(quiz)

    async def get_quiz_or_404(self, quiz_id: int) -> QuizFullResponse:
        quiz = await self.quiz_repo.get_full_quiz(quiz_id)
        if not quiz:
            raise NotFoundException("Quiz not found")
        return QuizFullResponse.model_validate(quiz)

    async def update_quiz(
        self, quiz_id: int, data: QuizUpdateRequest, user_id: int
    ) -> QuizFullResponse:
        quiz = await self.get_quiz_or_404(quiz_id)

        await self._check_company_permission(quiz.company_id, user_id)

        update_data = data.model_dump(exclude_none=True)

        updated = await self.quiz_repo.edit_one(quiz_id, update_data)

        full_quiz = await self.quiz_repo.get_full_quiz(updated["id"])
        return QuizFullResponse.model_validate(full_quiz)

    async def delete_quiz(self, quiz_id: int, user_id: int) -> QuizResponse:
        quiz = await self.get_quiz_or_404(quiz_id)

        await self._check_company_permission(quiz.company_id, user_id)

        deleted = await self.quiz_repo.delete_one(quiz_id)
        return QuizResponse.model_validate(deleted)

    async def get_company_quizzes(
        self, company_id: int, skip: int, limit: int
    ) -> QuizListResponse:
        quizzes = await self.quiz_repo.find_all(
            skip=skip, limit=limit, company_id=company_id
        )
        total = await self.quiz_repo.count_all(company_id=company_id)
        page = (skip // limit) + 1
        return QuizListResponse(
            items=[QuizResponse.model_validate(q) for q in quizzes],
            total=total,
            page=page,
            per_page=limit,
        )

    async def add_question(
        self, quiz_id: int, data: QuestionRequest, user_id: int
    ) -> QuizFullResponse:
        quiz = await self.get_quiz_or_404(quiz_id)

        await self._check_company_permission(quiz.company_id, user_id)

        question = await self.question_repo.add_one(
            {"title": data.title, "quiz_id": quiz_id}
        )

        answer_options_data = self._dump_answer_options(
            data.answer_options, question["id"]
        )

        await self.answer_repo.add_many(answer_options_data)

        full_quiz = await self.quiz_repo.get_full_quiz(quiz_id)
        return QuizFullResponse.model_validate(full_quiz)

    async def update_question(
        self, question_id: int, data: QuestionRequest, user_id: int
    ) -> QuizFullResponse:
        question = await self.question_repo.find_one(id=question_id)
        if not question:
            raise NotFoundException("Question not found")

        quiz = await self.get_quiz_or_404(question.quiz_id)

        await self._check_company_permission(quiz.company_id, user_id)

        if data.title:
            await self.question_repo.edit_one(question_id, {"title": data.title})

        await self.answer_repo.delete_answer_options(question_id=question_id)

        answer_options_data = self._dump_answer_options(
            data.answer_options, question.id
        )

        await self.answer_repo.add_many(answer_options_data)

        full_quiz = await self.quiz_repo.get_full_quiz(quiz.id)
        return QuizFullResponse.model_validate(full_quiz)

    async def delete_question(self, question_id: int, user_id: int) -> QuizFullResponse:
        question = await self.question_repo.find_one(id=question_id)
        if not question:
            raise NotFoundException("Question not found")

        quiz = await self.get_quiz_or_404(question.quiz_id)

        await self._check_company_permission(quiz.company_id, user_id)

        await self.question_repo.delete_one(question_id)

        full_quiz = await self.quiz_repo.get_full_quiz(quiz.id)
        return QuizFullResponse.model_validate(full_quiz)

    async def _check_company_permission(self, company_id: int, user_id: int) -> None:
        membership = await MembershipRepository(self.db).find_one(
            company_id=company_id, user_id=user_id
        )
        company = await CompanyRepository(self.db).find_one(id=company_id)
        if (
            not membership or membership.status != MembershipStatus.ADMIN
        ) and company.owner_id != user_id:
            raise ForbiddenException("You do not have permission.")

    def _dump_answer_options(
        self, data: list[AnswerOptionRequest], question_id: int
    ) -> dict:

        answer_options_data = [
            {
                "text": answer_option.text,
                "is_correct": answer_option.is_correct,
                "question_id": question_id,
            }
            for answer_option in data
        ]
        return answer_options_data
