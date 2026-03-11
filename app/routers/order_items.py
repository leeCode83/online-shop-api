from fastapi import APIRouter, Depends, HTTPException
from app.models.order_item import (
    OrderItemCreate, OrderItemUpdate, OrderItemResponse, AllOrderItemsResponse
)
from app.services.order_items import (
    create_order_item, update_order_item, delete_order_item,
    get_all_order_items, get_order_item_by_id
)
from app.services.auth import get_current_user, oauth2_scheme


router = APIRouter(prefix="/order-items", tags=["order-items"])


@router.post("/", response_model=OrderItemResponse)
def create_order_item_endpoint(
    order_item: OrderItemCreate,
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = create_order_item(order_item, token)
        if not response.data:
            raise HTTPException(
                status_code=500, detail="Failed to create order item"
            )
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id}", response_model=OrderItemResponse)
def update_order_item_endpoint(
    id: str,
    order_item: OrderItemUpdate,
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = update_order_item(id, order_item, token)
        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Order item not found or no changes made"
            )
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", response_model=OrderItemResponse)
def delete_order_item_endpoint(
    id: str,
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = delete_order_item(id, token)
        if not response.data:
            raise HTTPException(status_code=404, detail="Order item not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=AllOrderItemsResponse)
def get_all_order_items_endpoint():
    try:
        response = get_all_order_items()
        return {"order_items": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=OrderItemResponse)
def get_order_item_by_id_endpoint(id: str):
    try:
        response = get_order_item_by_id(id)
        if not response.data:
            raise HTTPException(status_code=404, detail="Order item not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
