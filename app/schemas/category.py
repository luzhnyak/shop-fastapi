from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator
import slugify


class CategoryBase(BaseModel):
    name: str
    slug: str | None = None
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    parent_id: Optional[int] = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CategoryList(BaseModel):
    items: List[CategoryRead]
    total: int
    page: int
    per_page: int
