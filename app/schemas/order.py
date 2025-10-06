from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float
    selected_options: Optional[dict] = None


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class OrderBase(BaseModel):
    address_id: int
    user_id: int
    status: OrderStatus = OrderStatus.pending
    total_price: float = 0.0


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    address_id: Optional[int]
    user_id: Optional[int]
    status: Optional[OrderStatus]
    total_price: Optional[float]


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    items: List[OrderItemRead] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class OrderReadMin(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class OrderList(BaseModel):
    items: List[OrderReadMin]
    total: int
    page: int
    per_page: int
