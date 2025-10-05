from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload, joinedload

from app.utils.repository import SQLAlchemyRepository
from app.models import Product, ProductImage, ProductOption


class ProductImageRepository(SQLAlchemyRepository):
    model = ProductImage


class ProductOptionRepository(SQLAlchemyRepository):
    model = ProductOption


class ProductRepository(SQLAlchemyRepository):
    model = Product
