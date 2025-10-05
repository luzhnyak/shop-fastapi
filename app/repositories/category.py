from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload, joinedload

from app.models import Category
from app.utils.repository import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository):
    model = Category
