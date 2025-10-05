from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class WishlistBase(BaseModel):
    product_id: int


class WishlistCreate(WishlistBase):
    pass


class WishlistUpdate(WishlistBase):
    pass


class WishlistRead(WishlistBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime


class WishlistList(BaseModel):
    items: List[WishlistRead]
    total: int
    page: int
    per_page: int
