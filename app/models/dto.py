from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional
from uuid import UUID
from datetime import datetime


# Address
class AddressOut(BaseModel):
    id: UUID
    created_at: datetime
    line1: str
    line2: str
    city: str
    state: constr(min_length=2, max_length=2)
    zip_code: str


# Customer
class CustomerOut(BaseModel):
    id: UUID
    email: EmailStr
    telephone: str
    first_name: str
    last_name: str
    created_at: datetime


# Orders
class OrderOut(BaseModel):
    id: UUID
    created_at: datetime
    store_id: Optional[UUID]
    pick_up: bool = True
    status: str
    billing_address: Optional[AddressOut]
    shipping_addresses: List[AddressOut]

    class Config:
        from_attributes = True


class AllOrdersOut(CustomerOut):
    orders: List[OrderOut]


class OrderCountByZipOut(BaseModel):
    zip_code: str
    count: int


class OrderCountsByZipOut(BaseModel):
    counts: List[OrderCountByZipOut]


class OrderCountByHourOut(BaseModel):
    hour: int
    count: int


class OrderCountsByHourOut(BaseModel):
    counts: List[OrderCountByHourOut]


class CustomerOrderCountOut(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    orders: int


class CustomerOrderCountsOut(BaseModel):
    counts: List[CustomerOrderCountOut]
