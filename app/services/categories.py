from app.models.category import CategoryCreate, CategoryUpdate
from app.database import supabase


def create_category(category: CategoryCreate, token: str):
    try:
        response = supabase.postgrest.auth(token).table("categories").insert(
            category.model_dump()
        ).execute()
        return response
    except Exception as e:
        raise e


def update_category(id: str, category: CategoryUpdate, token: str):
    try:
        update_data = category.model_dump(exclude_unset=True)
        response = supabase.postgrest.auth(token).table("categories").update(
            update_data
        ).eq("id", id).execute()
        return response
    except Exception as e:
        raise e


def delete_category(id: str, token: str):
    try:
        response = supabase.postgrest.auth(token).table("categories").delete(
        ).eq("id", id).execute()
        return response
    except Exception as e:
        raise e


def get_all_categories():

    try:
        response = supabase.table("categories").select(
            "id, name, description"
        ).execute()
        return response
    except Exception as e:
        raise e


def get_category_by_id(id: str):
    try:
        response = supabase.table("categories").select(
            "id, name, description"
        ).eq("id", id).execute()
        return response
    except Exception as e:
        raise e


def create_categories_batch(categories: list[CategoryCreate], token: str):
    try:
        data = [c.model_dump() for c in categories]
        response = supabase.postgrest.auth(token).table("categories").insert(
            data
        ).execute()
        return response
    except Exception as e:
        raise e
