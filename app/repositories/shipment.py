from sqlalchemy import func, select

from app.repositories.repository import SQLAlchemyRepository
from app.models import Shipment


class ShipmentRepository(SQLAlchemyRepository):
    model = Shipment
