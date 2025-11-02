from sqlalchemy import func, select
from sqlalchemy.orm import selectinload, joinedload

from app.db.error_handler import db_error_handler
from app.repositories.repository import SQLAlchemyRepository
from app.models.product import Product
from app.models import Cart, CartItem


class CartRepository(SQLAlchemyRepository):
    model = Cart

    @db_error_handler
    async def find_one_cart(self, **filter_by):
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.items),
            )
            .filter_by(**filter_by)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()


class CartItemRepository(SQLAlchemyRepository):
    model = CartItem

    @db_error_handler
    async def find_all_with_product(self, **filter_by):
        stmt = (
            select(self.model)
            .options(selectinload(self.model.product))
            .filter_by(**filter_by)
        )
        res = await self.session.execute(stmt)
        return res.scalars().all()
