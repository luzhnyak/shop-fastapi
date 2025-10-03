from typing import Optional
from pydantic import BaseModel, ConfigDict


class AddressBase(BaseModel):
    country: str
    city: str
    street: str
    postal_code: str
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    country: Optional[str]
    city: Optional[str]
    street: Optional[str]
    postal_code: Optional[str]
    is_default: Optional[bool]


class AddressRead(AddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
