from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderItemInput(BaseModel):
    product_id: int
    quantity: int
    price: float


class CreateTestOrderRequest(BaseModel):
    phone: str
    full_name: str

    address_line: str
    city: str
    state: str
    pincode: str

    items: List[OrderItemInput]
    delivery_charge: float
    payment_method: str

class PhoneCheckRequest(BaseModel):
    phone: str


class PhoneCheckResponse(BaseModel):
    exists: bool
    user_id: int | None = None

class OrderDetailedGridResponse(BaseModel):
    order_id: int
    customer_name: str
    contact_number: str
    full_address: str
    payment_method: str | None
    ordered_date: datetime
    product_name: str
    quantity: int
    price: float
    total_bill: float