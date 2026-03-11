from fastapi import APIRouter, Depends, HTTPException
from app.models.item import (
    ItemCreate, ItemUpdate, ItemResponse, AllItemsResponse
)
from app.services.items import (
    create_item, update_item, delete_item, get_all_items,
    get_item_by_id, create_items_batch
)
from app.services.auth import get_current_user, oauth2_scheme


router = APIRouter(prefix="/items", tags=["items"])


@router.post("/batch", response_model=list[ItemResponse])
def create_items_batch_endpoint(
    items: list[ItemCreate],
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = create_items_batch(items, token)
        if not response.data:
            raise HTTPException(
                status_code=500, detail="Failed to create items"
            )
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ItemResponse)
def create_item_endpoint(
    item: ItemCreate,
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = create_item(item, token)
        if not response.data:
            raise HTTPException(
                status_code=500, detail="Failed to create item"
            )
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id}", response_model=ItemResponse)
def update_item_endpoint(
    id: str,
    item: ItemUpdate,
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = update_item(id, item, token)
        if not response.data:
            raise HTTPException(
                status_code=404, detail="Item not found or no changes made"
            )
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", response_model=ItemResponse)
def delete_item_endpoint(
    id: str,
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = delete_item(id, token)
        if not response.data:
            raise HTTPException(status_code=404, detail="Item not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=AllItemsResponse)
def get_all_items_endpoint():
    try:
        response = get_all_items()
        return {"items": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=ItemResponse)
def get_item_by_id_endpoint(id: str):
    try:
        response = get_item_by_id(id)
        if not response.data:
            raise HTTPException(status_code=404, detail="Item not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
