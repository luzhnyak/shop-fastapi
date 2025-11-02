from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class CartItemBase(BaseModel):
    product_id: int
    quantity: int
    selected_options: Optional[dict] = None


class CartItemCreate(CartItemBase):
    pass


class CartItemRead(CartItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None


class CartBase(BaseModel):
    user_id: int
    items: List[CartItemCreate] = []
    created_at: datetime
    updated_at: datetime


class CartCreate(CartBase):
    pass


class CartUpdate(BaseModel):
    items: Optional[List[CartItemCreate]] = None


class CartDelete(BaseModel):
    product_id: int


class CartRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    items: List[CartItemRead] = []


class CartReadMin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class CartList(BaseModel):
    items: List[CartReadMin] = []
    total: int
    page: int
    per_page: int
