from app.models.order import OrderUpdate
from app.database import supabase


def create_order(user_id: str, items: list, token: str):
    try:
        # items: [{"item_id": "...", "quantity": ...}]
        response = supabase.postgrest.auth(token).rpc(
            "create_order_with_items",
            {
                "p_user_id": user_id,
                "p_items": items
            }
        ).execute()
        return response
    except Exception as e:
        raise e


def update_order(id: str, order: OrderUpdate, token: str):

    try:
        update_data = order.model_dump(exclude_unset=True)
        response = supabase.postgrest.auth(token).table("orders").update(
            update_data
        ).eq("id", id).execute()
        return response
    except Exception as e:
        raise e


def delete_order(id: str, token: str):
    try:
        response = supabase.postgrest.auth(token).table("orders").delete().eq(
            "id", id
        ).execute()
        return response
    except Exception as e:
        raise e


def get_all_orders():
    try:
        response = supabase.table("orders").select("*").execute()
        return response
    except Exception as e:
        raise e


def get_order_by_id(id: str):
    try:
        response = supabase.table("orders").select("*").eq("id", id).execute()
        return response
    except Exception as e:
        raise e


def get_orders_by_user(user_id: str):
    try:
        response = supabase.table("orders").select("*").eq(
            "user_id", user_id
        ).execute()
        return response
    except Exception as e:
        raise e
