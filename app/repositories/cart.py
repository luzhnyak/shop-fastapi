from sqlalchemy import func, select

from app.utils.repository import SQLAlchemyRepository
from app.models import Cart, CartItem


class CartRepository(SQLAlchemyRepository):
    model = Cart


class CartItemRepository(SQLAlchemyRepository):
    model = CartItem
