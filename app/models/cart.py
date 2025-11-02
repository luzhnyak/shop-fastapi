from typing import List, Optional

from sqlalchemy import (
    Integer,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base
from app.models.base_model import BaseModel


class Cart(BaseModel):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    items: Mapped[List["CartItem"]] = relationship(back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    selected_options: Mapped[Optional[dict]] = mapped_column(JSON)

    cart: Mapped["Cart"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship("Product", lazy="joined")  # type: ignore
