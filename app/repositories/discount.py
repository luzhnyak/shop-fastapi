from sqlalchemy import func, select

from app.repositories.repository import SQLAlchemyRepository
from app.models import Discount


class DiscountRepository(SQLAlchemyRepository):
    model = Discount
