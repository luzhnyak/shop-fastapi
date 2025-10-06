from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload, joinedload

from app.models import Category
from app.repositories.repository import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository):
    model = Category
