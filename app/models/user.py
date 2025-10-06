from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Enum, Integer, String
import enum

from app.models.base_model import BaseModel


class Role(enum.Enum):
    admin = "admin"
    customer = "customer"
    manager = "manager"


class User(BaseModel):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.customer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")  # type: ignore
    orders: Mapped[List["Order"]] = relationship(back_populates="user")  # type: ignore
    reviews: Mapped[List["Review"]] = relationship(back_populates="user")  # type: ignore
    wishlist: Mapped[List["Wishlist"]] = relationship(back_populates="user")  # type: ignore
    custom_orders: Mapped[List["CustomOrder"]] = relationship(back_populates="user")  # type: ignore
