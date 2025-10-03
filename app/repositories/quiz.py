from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload, joinedload
from app.models.quiz import AnswerOption, Question, Quiz, QuizResult
from app.utils.repository import SQLAlchemyRepository


class QuizRepository(SQLAlchemyRepository):
    model = Quiz

    async def get_full_quiz(self, quiz_id: int) -> Quiz:
        stmt = (
            select(Quiz)
            .options(selectinload(Quiz.questions).selectinload(Question.answer_options))
            .where(Quiz.id == quiz_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class QuestionRepository(SQLAlchemyRepository):
    model = Question

    async def get_full_question(self, question_id: int) -> dict:
        stmt = (
            select(Question)
            .options(joinedload(Question.answer_options))
            .where(Question.id == question_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class AnswerOptionRepository(SQLAlchemyRepository):
    model = AnswerOption

    async def delete_answer_options(self, question_id: int):
        stmt = delete(self.model).where(self.model.question_id == question_id)
        await self.session.execute(stmt)
        await self.session.commit()


class QuizResultRepository(SQLAlchemyRepository):
    model = QuizResult

    async def find_all(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalars().all()
