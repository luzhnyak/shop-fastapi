from sqlalchemy import func, select

from app.repositories.repository import SQLAlchemyRepository
from app.models import Address


class AdressRepository(SQLAlchemyRepository):
    model = Address
