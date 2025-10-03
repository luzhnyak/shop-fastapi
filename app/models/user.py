from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Integer, String
import enum

from app.models.address import Address
from app.models.base_model import BaseModel
from app.models.custom_order import CustomOrder
from app.models.order import Order
from app.models.review import Review
from app.models.wishlist import Wishlist


class Role(enum.Enum):
    admin = "admin"
    сustomer = "customer"
    manager = "manager"


class User(BaseModel):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[Role] = mapped_column(String, default=Role.customer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    orders: Mapped[List["Order"]] = relationship(back_populates="user")
    reviews: Mapped[List["Review"]] = relationship(back_populates="user")
    wishlist: Mapped[List["Wishlist"]] = relationship(back_populates="user")
    custom_orders: Mapped[List["CustomOrder"]] = relationship(back_populates="user")
