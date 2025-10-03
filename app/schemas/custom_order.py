from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.models.custom_order import CustomOrderStatus


class CustomOrderBase(BaseModel):
    description: str
    dimensions: Optional[dict] = None
    material: Optional[str] = None
    images: Optional[List[str]] = None
    status: CustomOrderStatus = CustomOrderStatus.pending
    estimated_price: Optional[float] = None


class CustomOrderCreate(CustomOrderBase):
    pass


class CustomOrderRead(CustomOrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
