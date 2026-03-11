from app.models.order_item import OrderItemCreate, OrderItemUpdate
from app.database import supabase


def create_order_item(order_item: OrderItemCreate, token: str):
    try:
        response = supabase.postgrest.auth(token).table("order_item").insert(
            order_item.model_dump()
        ).execute()
        return response
    except Exception as e:
        raise e


def update_order_item(id: str, order_item: OrderItemUpdate, token: str):
    try:
        update_data = order_item.model_dump(exclude_unset=True)
        response = supabase.postgrest.auth(token).table("order_item").update(
            update_data
        ).eq("id", id).execute()
        return response
    except Exception as e:
        raise e


def delete_order_item(id: str, token: str):
    try:
        response = supabase.postgrest.auth(token).table("order_item").delete(
        ).eq("id", id).execute()
        return response
    except Exception as e:
        raise e


def get_all_order_items():

    try:
        response = supabase.table("order_item").select("*").execute()
        return response
    except Exception as e:
        raise e


def get_order_item_by_id(id: str):
    try:
        response = supabase.table("order_item").select("*").eq(
            "id", id
        ).execute()
        return response
    except Exception as e:
        raise e
