from pydantic import BaseModel, Field
from typing import Optional


class OrderItem(BaseModel):
    item_id: str
    order_id: str
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)


class OrderItemCreate(OrderItem):
    pass


class OrderItemUpdate(BaseModel):
    item_id: Optional[str] = None
    order_id: Optional[str] = None
    quantity: Optional[int] = Field(None, gt=0)
    unit_price: Optional[float] = Field(None, ge=0)


class OrderItemResponse(OrderItem):
    id: str


class AllOrderItemsResponse(BaseModel):
    order_items: list[OrderItemResponse]
