from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ProductOptionBase(BaseModel):
    name: str
    value: str
    additional_price: float = 0.0


class ProductOptionCreate(ProductOptionBase):
    pass


class ProductOptionRead(ProductOptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProductImageBase(BaseModel):
    image_url: str
    is_main: bool = False


class ProductImageCreate(ProductImageBase):
    pass


class ProductImageRead(ProductImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    base_price: float
    sku: Optional[str] = None
    stock_quantity: int = 0


class ProductCreate(ProductBase):
    options: Optional[List[ProductOptionCreate]] = []
    images: Optional[List[ProductImageCreate]] = []


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    category_id: Optional[int]
    base_price: Optional[float]
    sku: Optional[str]
    stock_quantity: Optional[int]


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    options: List[ProductOptionRead] = []
    images: List[ProductImageRead] = []


class ProductList(BaseModel):
    items: List[ProductRead]
    total: int
    page: int
    per_page: int
