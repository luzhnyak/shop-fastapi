from sqlalchemy import func, select

from app.utils.repository import SQLAlchemyRepository
from app.models import Order, OrderItem, OrderStatus


class OrderRepository(SQLAlchemyRepository):
    model = Order


class OrderItemRepository(SQLAlchemyRepository):
    model = OrderItem
