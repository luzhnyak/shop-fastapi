from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload, joinedload

from app.db.error_handler import db_error_handler
from app.repositories.repository import SQLAlchemyRepository
from app.models import Product, ProductImage, ProductOption


class ProductImageRepository(SQLAlchemyRepository):
    model = ProductImage


class ProductOptionRepository(SQLAlchemyRepository):
    model = ProductOption


class ProductRepository(SQLAlchemyRepository):
    model = Product

    @db_error_handler
    async def find_one_product(self, **filter_by):
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.options),
                selectinload(self.model.images),
            )
            .filter_by(**filter_by)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    @db_error_handler
    async def find_many_products(self, skip: int, limit: int, **filter_by):
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.options),
                selectinload(self.model.images),
            )
            .filter_by(**filter_by)
        )
        res = await self.session.execute(stmt.offset(skip).limit(limit))
        return res.scalars().all()

    @db_error_handler
    async def find_all_products(self, **filter_by):
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.options),
                selectinload(self.model.images),
            )
            .filter_by(**filter_by)
        )
        res = await self.session.execute(stmt)
        return res.scalars().all()
