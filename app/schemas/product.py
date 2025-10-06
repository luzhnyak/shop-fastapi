from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


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
    base_price: float = 0.0
    sku: Optional[str] = None
    stock_quantity: int = 0


class ProductCreate(ProductBase):
    options: Optional[List[ProductOptionCreate]] = Field(default_factory=list)
    images: Optional[List[ProductImageCreate]] = Field(default_factory=list)


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
    options: Optional[List[ProductOptionRead]] = Field(default_factory=list)
    images: Optional[List[ProductImageRead]] = Field(default_factory=list)


class ProductList(BaseModel):
    items: List[ProductRead]
    total: int
    page: int
    per_page: int
