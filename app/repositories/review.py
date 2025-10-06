from sqlalchemy import func, select

from app.repositories.repository import SQLAlchemyRepository
from app.models import Review


class ReviewRepository(SQLAlchemyRepository):
    model = Review
