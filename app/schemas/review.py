from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    product_id: int
    rating: int
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
