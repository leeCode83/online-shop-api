from fastapi import APIRouter, Depends, HTTPException
from app.models.category import (
    CategoryCreate, CategoryUpdate, CategoryResponse, AllCategoriesResponse
)
from app.services.categories import (
    create_category, update_category, delete_category,
    get_all_categories, get_category_by_id, create_categories_batch
)
from app.services.auth import get_current_user, oauth2_scheme


router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/batch", response_model=list[CategoryResponse])
def create_categories_batch_endpoint(
    categories: list[CategoryCreate],
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = create_categories_batch(categories, token)
        if not response.data:
            raise HTTPException(
                status_code=500, detail="Failed to create categories"
            )
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=CategoryResponse)
def create_category_endpoint(
    category: CategoryCreate,
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = create_category(category, token)
        if not response.data:
            raise HTTPException(
                status_code=500, detail="Failed to create category"
            )
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id}", response_model=CategoryResponse)
def update_category_endpoint(
    id: str,
    category: CategoryUpdate,
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = update_category(id, category, token)
        if not response.data:
            raise HTTPException(
                status_code=404, detail="Category not found or no changes made"
            )
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", response_model=CategoryResponse)
def delete_category_endpoint(
    id: str,
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = delete_category(id, token)
        if not response.data:
            raise HTTPException(status_code=404, detail="Category not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=AllCategoriesResponse)
def get_all_categories_endpoint():
    try:
        response = get_all_categories()
        return {"categories": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=CategoryResponse)
def get_category_by_id_endpoint(id: str):
    try:
        response = get_category_by_id(id)
        if not response.data:
            raise HTTPException(status_code=404, detail="Category not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
