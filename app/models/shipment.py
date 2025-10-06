import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Enum,
    String,
    Integer,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

from app.db.db import Base


class ShipmentStatus(enum.Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    provider: Mapped[str] = mapped_column(String, nullable=False)
    tracking_number: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[ShipmentStatus] = mapped_column(
        Enum(ShipmentStatus), default=ShipmentStatus.pending
    )
    shipped_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    order: Mapped["Order"] = relationship(back_populates="shipment")  # type: ignore
