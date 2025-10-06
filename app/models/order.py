import enum
from typing import List, Optional

from sqlalchemy import (
    Enum,
    String,
    Integer,
    ForeignKey,
    Float,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base
from app.models.base_model import BaseModel


class OrderStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(BaseModel):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.pending
    )
    total_price: Mapped[float] = mapped_column(Float, default=0)

    user: Mapped["User"] = relationship(back_populates="orders")  # type: ignore
    address: Mapped["Address"] = relationship(back_populates="orders")  # type: ignore
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order")
    shipment: Mapped["Shipment"] = relationship(back_populates="order", uselist=False)  # type: ignore


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    price: Mapped[float] = mapped_column(Float, default=0)
    selected_options: Mapped[Optional[dict]] = mapped_column(JSON)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items")  # type: ignore
