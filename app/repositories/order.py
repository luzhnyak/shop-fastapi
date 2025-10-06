from sqlalchemy import func, select
from sqlalchemy.orm import selectinload, joinedload

from app.db.error_handler import db_error_handler
from app.repositories.repository import SQLAlchemyRepository
from app.models import Order, OrderItem, OrderStatus


class OrderItemRepository(SQLAlchemyRepository):
    model = OrderItem


class OrderRepository(SQLAlchemyRepository):
    model = Order

    @db_error_handler
    async def find_one_order(self, **filter_by):
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.items),
            )
            .filter_by(**filter_by)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
