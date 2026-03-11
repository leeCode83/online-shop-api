from app.models.item import ItemCreate, ItemUpdate
from app.database import supabase


def create_item(item: ItemCreate, token: str):
    try:
        response = supabase.postgrest.auth(token).table("items").insert(
            item.model_dump()
        ).execute()
        return response
    except Exception as e:
        raise e


def update_item(id: str, item: ItemUpdate, token: str):
    try:
        update_data = item.model_dump(exclude_unset=True)
        response = supabase.postgrest.auth(token).table("items").update(
            update_data
        ).eq("id", id).execute()
        return response
    except Exception as e:
        raise e


def delete_item(id: str, token: str):
    try:
        response = supabase.postgrest.auth(token).table("items").delete().eq(
            "id", id
        ).execute()
        return response
    except Exception as e:
        raise e


def get_all_items():
    try:
        response = supabase.table("items").select("*").execute()
        return response
    except Exception as e:
        raise e


def get_item_by_id(id: str):
    try:
        response = supabase.table("items").select("*").eq("id", id).execute()
        return response
    except Exception as e:
        raise e


def create_items_batch(items: list[ItemCreate], token: str):
    try:
        data = [i.model_dump() for i in items]
        response = supabase.postgrest.auth(token).table("items").insert(
            data
        ).execute()
        return response
    except Exception as e:
        raise e
