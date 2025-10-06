from sqlalchemy import func, select

from app.repositories.repository import SQLAlchemyRepository
from app.models import Wishlist


class WishlistRepository(SQLAlchemyRepository):
    model = Wishlist
