from pydantic import BaseModel, Field
from typing import Optional


class Item(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10, max_length=1000)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category_id: str


class ItemCreate(Item):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category_id: Optional[str] = None


class ItemResponse(Item):
    id: str


class AllItemsResponse(BaseModel):
    items: list[ItemResponse]
