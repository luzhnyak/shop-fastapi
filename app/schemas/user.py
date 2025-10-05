from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Optional

from app.models.user import Role


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: Role = Role.customer
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    role: Optional[Role]
    is_active: Optional[bool]


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class UserList(BaseModel):
    items: List[UserRead]
    total: int
    page: int
    per_page: int
