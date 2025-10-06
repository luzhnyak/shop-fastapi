from sqlalchemy import func, select

from app.repositories.repository import SQLAlchemyRepository
from app.models import CustomOrder


class CustomOrderRepository(SQLAlchemyRepository):
    model = CustomOrder
