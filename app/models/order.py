from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class PaymentStatus(str, Enum):
    UNPAID = "unpaid"
    PAID = "paid"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class CheckoutItem(BaseModel):
    item_id: str
    quantity: int


class CheckoutRequest(BaseModel):
    items: list[CheckoutItem]


class Order(BaseModel):
    user_id: str
    total_price: float = Field(..., ge=0)
    payment_status: PaymentStatus = Field(default=PaymentStatus.UNPAID)


class OrderCreate(Order):
    pass


class OrderUpdate(BaseModel):
    user_id: Optional[str] = None
    total_price: Optional[float] = Field(None, ge=0)
    payment_status: Optional[PaymentStatus] = None


class OrderResponse(Order):
    id: str
    created_at: Optional[str] = None


class AllOrdersResponse(BaseModel):
    orders: list[OrderResponse]
