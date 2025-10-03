from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.models.order import OrderStatus


class CartItemBase(BaseModel):
    product_id: int
    quantity: int
    selected_options: Optional[dict] = None


class CartItemCreate(CartItemBase):
    pass


class CartItemRead(CartItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CartRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    items: List[CartItemRead] = []
    created_at: datetime
    updated_at: datetime


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
    status: OrderStatus = OrderStatus.pending
    total_price: float = 0.0


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    items: List[OrderItemRead] = []
    created_at: datetime
    updated_at: datetime
