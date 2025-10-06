import enum
from typing import Optional

from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    Text,
    Float,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class CustomOrderStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class CustomOrder(BaseModel):
    __tablename__ = "custom_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    description: Mapped[str] = mapped_column(Text, nullable=False)
    dimensions: Mapped[Optional[dict]] = mapped_column(JSON)  # {length, width, height}
    material: Mapped[Optional[str]] = mapped_column(String)
    images: Mapped[Optional[list]] = mapped_column(JSON)  # список URL або шляхів
    status: Mapped[CustomOrderStatus] = mapped_column(
        String, default=CustomOrderStatus.pending
    )
    estimated_price: Mapped[Optional[float]] = mapped_column(Float)

    user: Mapped["User"] = relationship(back_populates="custom_orders")  # type: ignore
