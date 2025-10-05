from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.models.shipment import ShipmentStatus


class ShipmentBase(BaseModel):
    provider: str
    tracking_number: Optional[str] = None
    status: ShipmentStatus = ShipmentStatus.pending


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(ShipmentBase):
    provider: Optional[str]
    tracking_number: Optional[str]
    status: Optional[ShipmentStatus]


class ShipmentRead(ShipmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    shipped_at: Optional[datetime]
    delivered_at: Optional[datetime]


class ShipmentList(BaseModel):
    items: List[ShipmentRead]
    total: int
    page: int
    per_page: int
