from pydantic import BaseModel, Field
from typing import Optional


class Category(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=5, max_length=255)


class CategoryCreate(Category):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=5, max_length=255)


class CategoryResponse(Category):
    id: str


class AllCategoriesResponse(BaseModel):
    categories: list[CategoryResponse]
