import csv
import io
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenException
from app.db.redis import RedisService
from app.models.membership import MembershipStatus
from app.models.user import User
from app.services.company import CompanyService
from app.services.membership import MembershipService
from app.services.quiz import QuizService
from app.services.quiz_result_redis import QuizResultRedisService


class QuizExportService:

    def __init__(self, db: AsyncSession, redis_service: RedisService):
        self.redis_service = redis_service
        self.quiz_service = QuizService(db)
        self.company_service = CompanyService(db)
        self.membership_service = MembershipService(db)
        self.quiz_result_redis_service = QuizResultRedisService(db, redis_service)

    async def _check_permission(
        self, quiz_id: int, user_id: int, current_user_id: int
    ) -> None:
        quiz = await self.quiz_service.get_quiz_or_404(quiz_id)
        company = await self.company_service.get_company(quiz.company_id)
        membership = await self.membership_service.get_membership(
            company.id, current_user_id
        )

        is_owner = company.owner_id == current_user_id
        is_admin = membership.status == MembershipStatus.ADMIN
        is_self = user_id == current_user_id

        if not (is_owner or is_admin or is_self):
            raise ForbiddenException("You do not have permission.")

    async def export_as_json(
        self, current_user: User, user_id: Optional[int], quiz_id: Optional[int]
    ):
        await self._check_permission(quiz_id, user_id, current_user.id)

        data = await self.quiz_result_redis_service.get_quiz_attempts_with_text(
            user_id, quiz_id
        )

        return data

    async def export_as_csv(
        self, current_user: User, user_id: Optional[int], quiz_id: Optional[int]
    ) -> io.StringIO:
        await self._check_permission(quiz_id, user_id, current_user.id)

        attempts = await self.quiz_result_redis_service.get_quiz_attempts_with_text(
            user_id, quiz_id
        )

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                "User ID",
                "Quiz Title",
                "Quiz Description",
                "Timestamp",
                "Question ID",
                "Question Title",
                "Answer Option ID",
                "Answer Option Text",
                "Is Correct",
            ]
        )

        for attempt in attempts:
            for answer in attempt["answers"]:
                question_id = answer["question_id"]
                question_title = answer["question_title"]

                for selected in answer["selected_answers"]:
                    writer.writerow(
                        [
                            attempt["user_id"],
                            attempt["quiz_title"],
                            attempt["quiz_description"],
                            attempt["timestamp"],
                            question_id,
                            question_title,
                            selected["id"],
                            selected["answer_option_text"],
                            selected["is_correct"],
                        ]
                    )

        return output.getvalue()
