from fastapi import APIRouter, Depends, HTTPException
from app.models.order import (
    OrderUpdate, OrderResponse, AllOrdersResponse, CheckoutRequest
)
from app.services.orders import (
    create_order, update_order, delete_order, get_all_orders,
    get_order_by_id, get_orders_by_user
)
from app.services.auth import get_current_user, oauth2_scheme


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/")
def create_order_endpoint(
    request: CheckoutRequest,
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        items_data = [item.model_dump() for item in request.items]
        response = create_order(str(current_user.id), items_data, token)
        if not response.data:
            raise HTTPException(
                status_code=500, detail="Failed to create order"
            )
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id}", response_model=OrderResponse)
def update_order_endpoint(
    id: str,
    order: OrderUpdate,
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = update_order(id, order, token)
        if not response.data:
            raise HTTPException(
                status_code=404, detail="Order not found or no changes made"
            )
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", response_model=OrderResponse)
def delete_order_endpoint(
    id: str,
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user)
):
    try:
        response = delete_order(id, token)
        if not response.data:
            raise HTTPException(status_code=404, detail="Order not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=AllOrdersResponse)
def get_all_orders_endpoint():
    try:
        response = get_all_orders()
        return {"orders": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=OrderResponse)
def get_order_by_id_endpoint(id: str):
    try:
        response = get_order_by_id(id)
        if not response.data:
            raise HTTPException(status_code=404, detail="Order not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}", response_model=AllOrdersResponse)
def get_orders_by_user_endpoint(user_id: str):
    try:
        response = get_orders_by_user(user_id)
        return {"orders": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
