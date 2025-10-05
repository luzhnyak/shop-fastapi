from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class DiscountBase(BaseModel):
    code: str
    description: Optional[str] = None
    discount_type: str  # "percent" | "fixed"
    value: float
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    is_active: bool = True


class DiscountCreate(DiscountBase):
    pass


class DiscountUpdate(DiscountBase):
    pass


class DiscountRead(DiscountBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class DiscountList(BaseModel):
    items: List[DiscountRead]
    total: int
    page: int
    per_page: int
