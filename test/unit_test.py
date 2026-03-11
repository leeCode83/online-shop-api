import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.services.auth import create_new_user, login, get_current_user
from app.services.categories import (
    create_category, update_category, delete_category,
    get_all_categories, get_category_by_id
)
from app.services.items import (
    create_item, update_item, delete_item,
    get_all_items, get_item_by_id
)
from app.models.category import CategoryCreate, CategoryUpdate
from app.models.item import ItemCreate, ItemUpdate
from app.services.orders import (
    create_order, update_order, delete_order,
    get_all_orders, get_order_by_id, get_orders_by_user
)
from app.models.order import OrderUpdate


# --- Auth Service Tests ---

@patch("app.services.auth.supabase")
def test_create_new_user_success(mock_supabase):
    # Mock successful sign up
    mock_supabase.auth.sign_up.return_value = {
        "id": "user_123", "email": "test@example.com"
    }

    result = create_new_user("test@example.com", "password123")

    assert result == {"id": "user_123", "email": "test@example.com"}
    mock_supabase.auth.sign_up.assert_called_once_with(
        {"email": "test@example.com", "password": "password123"}
    )


@patch("app.services.auth.supabase")
def test_create_new_user_failure(mock_supabase):
    # Mock exception during sign up
    mock_supabase.auth.sign_up.side_effect = Exception("Email already exists")

    with pytest.raises(Exception) as excinfo:
        create_new_user("test@example.com", "password123")

    assert str(excinfo.value) == "Email already exists"


@patch("app.services.auth.supabase")
def test_login_success(mock_supabase):
    # Mock successful login
    mock_supabase.auth.sign_in_with_password.return_value = {
        "session": {"access_token": "token123"}
    }

    result = login("test@example.com", "password123")

    assert result["session"]["access_token"] == "token123"


@patch("app.services.auth.supabase")
def test_login_failure(mock_supabase):
    # Mock invalid credentials
    mock_supabase.auth.sign_in_with_password.side_effect = Exception(
        "Invalid credentials"
    )

    with pytest.raises(Exception) as excinfo:
        login("test@example.com", "wrong_password")

    assert str(excinfo.value) == "Invalid credentials"


@patch("app.services.auth.supabase")
def test_get_current_user_success(mock_supabase):
    # Mock getting current user
    mock_user = MagicMock()
    mock_user.user = {"id": "user_123"}
    mock_supabase.auth.get_user.return_value = mock_user

    result = get_current_user("token123")

    assert result == {"id": "user_123"}


@patch("app.services.auth.supabase")
def test_get_current_user_failure(mock_supabase):
    # Mock invalid token
    mock_supabase.auth.get_user.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_current_user("invalid_token")

    assert excinfo.value.status_code == 401


# --- Categories Service Tests ---

@patch("app.services.categories.supabase")
def test_create_category_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = {"id": "cat_1", "name": "Electronics"}

    mock_supabase.postgrest.auth.return_value.table.return_value.insert.\
        return_value = mock_execute

    category_data = CategoryCreate(name="Electronics", description="Gadgets")
    result = create_category(category_data, "token123")

    assert result == {"id": "cat_1", "name": "Electronics"}


@patch("app.services.categories.supabase")
def test_update_category_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = {"id": "cat_1", "name": "Updated Name"}

    mock_supabase.postgrest.auth.return_value.table.return_value.update.\
        return_value.eq.return_value = mock_execute

    update_data = CategoryUpdate(name="Updated Name")
    result = update_category("cat_1", update_data, "token123")

    assert result == {"id": "cat_1", "name": "Updated Name"}


@patch("app.services.categories.supabase")
def test_delete_category_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = {"status": "success"}

    mock_supabase.postgrest.auth.return_value.table.return_value.delete.\
        return_value.eq.return_value = mock_execute

    result = delete_category("cat_1", "token123")

    assert result == {"status": "success"}


@patch("app.services.categories.supabase")
def test_get_all_categories_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = [
        {"id": "1", "name": "A"}, {"id": "2", "name": "B"}
    ]

    mock_supabase.table.return_value.select.return_value = mock_execute

    result = get_all_categories()

    assert len(result) == 2
    assert result[0]["name"] == "A"


@patch("app.services.categories.supabase")
def test_get_category_by_id_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = {"id": "1", "name": "A"}

    mock_supabase.table.return_value.select.return_value.eq.return_value = \
        mock_execute

    result = get_category_by_id("1")

    assert result == {"id": "1", "name": "A"}


@patch("app.services.categories.supabase")
def test_get_category_by_id_failure(mock_supabase):
    # Mock error scenario
    mock_supabase.table.return_value.select.return_value.eq.return_value.\
        execute.side_effect = Exception("Not found")

    with pytest.raises(Exception) as excinfo:
        get_category_by_id("999")

    assert str(excinfo.value) == "Not found"


# --- Items Service Tests ---

@patch("app.services.items.supabase")
def test_create_item_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = {"id": "item_1", "name": "Laptop"}

    mock_supabase.postgrest.auth.return_value.table.return_value.insert.\
        return_value = mock_execute

    item_data = ItemCreate(
        name="Laptop", description="High performance laptop",
        price=1500.0, stock=10, category_id="cat_1"
    )
    result = create_item(item_data, "token123")

    assert result == {"id": "item_1", "name": "Laptop"}


@patch("app.services.items.supabase")
def test_update_item_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = {
        "id": "item_1", "name": "Updated Laptop"
    }

    mock_supabase.postgrest.auth.return_value.table.return_value.update.\
        return_value.eq.return_value = mock_execute

    update_data = ItemUpdate(name="Updated Laptop")
    result = update_item("item_1", update_data, "token123")

    assert result == {"id": "item_1", "name": "Updated Laptop"}


@patch("app.services.items.supabase")
def test_delete_item_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = {"status": "success"}

    mock_supabase.postgrest.auth.return_value.table.return_value.delete.\
        return_value.eq.return_value = mock_execute

    result = delete_item("item_1", "token123")

    assert result == {"status": "success"}


@patch("app.services.items.supabase")
def test_get_all_items_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = [
        {"id": "1", "name": "A"}, {"id": "2", "name": "B"}
    ]

    mock_supabase.table.return_value.select.return_value = mock_execute

    result = get_all_items()

    assert len(result) == 2
    assert result[0]["name"] == "A"


@patch("app.services.items.supabase")
def test_get_item_by_id_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = {"id": "1", "name": "A"}

    mock_supabase.table.return_value.select.return_value.eq.return_value = \
        mock_execute

    result = get_item_by_id("1")

    assert result == {"id": "1", "name": "A"}


@patch("app.services.items.supabase")
def test_create_item_failure(mock_supabase):
    mock_supabase.postgrest.auth.return_value.table.return_value.insert.\
        return_value.execute.side_effect = Exception("Database error")

    item_data = ItemCreate(
        name="Laptop", description="High performance laptop",
        price=1500.0, stock=10, category_id="cat_1"
    )
    with pytest.raises(Exception) as excinfo:
        create_item(item_data, "token123")

    assert str(excinfo.value) == "Database error"


@patch("app.services.items.supabase")
def test_update_item_failure(mock_supabase):
    mock_supabase.postgrest.auth.return_value.table.return_value.update.\
        return_value.eq.return_value.execute.side_effect = Exception(
            "Update failed"
        )

    update_data = ItemUpdate(name="Updated Laptop")
    with pytest.raises(Exception) as excinfo:
        update_item("item_1", update_data, "token123")

    assert str(excinfo.value) == "Update failed"


@patch("app.services.items.supabase")
def test_delete_item_failure(mock_supabase):
    mock_supabase.postgrest.auth.return_value.table.return_value.delete.\
        return_value.eq.return_value.execute.side_effect = Exception(
            "Delete failed"
        )

    with pytest.raises(Exception) as excinfo:
        delete_item("item_1", "token123")

    assert str(excinfo.value) == "Delete failed"


@patch("app.services.items.supabase")
def test_get_all_items_failure(mock_supabase):
    mock_supabase.table.return_value.select.return_value.execute.\
        side_effect = Exception("Fetch failed")

    with pytest.raises(Exception) as excinfo:
        get_all_items()

    assert str(excinfo.value) == "Fetch failed"


@patch("app.services.items.supabase")
def test_get_item_by_id_failure(mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.\
        execute.side_effect = Exception("Item not found")

    with pytest.raises(Exception) as excinfo:
        get_item_by_id("999")

    assert str(excinfo.value) == "Item not found"


# --- Orders Service Tests ---

@patch("app.services.orders.supabase")
def test_create_order_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = {"id": "order_1", "status": "unpaid"}

    mock_supabase.postgrest.auth.return_value.rpc.return_value = mock_execute

    result = create_order(
        "user_123", [{"item_id": "item_1", "quantity": 2}], "token123"
    )

    assert result == {"id": "order_1", "status": "unpaid"}


@patch("app.services.orders.supabase")
def test_create_order_failure(mock_supabase):
    mock_supabase.postgrest.auth.return_value.rpc.return_value.execute.\
        side_effect = Exception("RPC failed")

    with pytest.raises(Exception) as excinfo:
        create_order(
            "user_123", [{"item_id": "item_1", "quantity": 2}], "token123"
        )

    assert str(excinfo.value) == "RPC failed"


@patch("app.services.orders.supabase")
def test_update_order_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = {
        "id": "order_1", "payment_status": "paid"
    }

    mock_supabase.postgrest.auth.return_value.table.return_value.update.\
        return_value.eq.return_value = mock_execute

    update_data = OrderUpdate(payment_status="paid")
    result = update_order("order_1", update_data, "token123")

    assert result == {"id": "order_1", "payment_status": "paid"}


@patch("app.services.orders.supabase")
def test_update_order_failure(mock_supabase):
    mock_supabase.postgrest.auth.return_value.table.return_value.update.\
        return_value.eq.return_value.execute.side_effect = Exception(
            "Update failed"
        )

    update_data = OrderUpdate(payment_status="paid")
    with pytest.raises(Exception) as excinfo:
        update_order("order_1", update_data, "token123")

    assert str(excinfo.value) == "Update failed"


@patch("app.services.orders.supabase")
def test_delete_order_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = {"status": "success"}

    mock_supabase.postgrest.auth.return_value.table.return_value.delete.\
        return_value.eq.return_value = mock_execute

    result = delete_order("order_1", "token123")

    assert result == {"status": "success"}


@patch("app.services.orders.supabase")
def test_delete_order_failure(mock_supabase):
    mock_supabase.postgrest.auth.return_value.table.return_value.delete.\
        return_value.eq.return_value.execute.side_effect = Exception(
            "Delete failed"
        )

    with pytest.raises(Exception) as excinfo:
        delete_order("order_1", "token123")

    assert str(excinfo.value) == "Delete failed"


@patch("app.services.orders.supabase")
def test_get_all_orders_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = [{"id": "1"}, {"id": "2"}]

    mock_supabase.table.return_value.select.return_value = mock_execute

    result = get_all_orders()

    assert len(result) == 2


@patch("app.services.orders.supabase")
def test_get_all_orders_failure(mock_supabase):
    mock_supabase.table.return_value.select.return_value.execute.\
        side_effect = Exception("Fetch failed")

    with pytest.raises(Exception) as excinfo:
        get_all_orders()

    assert str(excinfo.value) == "Fetch failed"


@patch("app.services.orders.supabase")
def test_get_order_by_id_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = {"id": "1"}

    mock_supabase.table.return_value.select.return_value.eq.return_value = \
        mock_execute

    result = get_order_by_id("1")

    assert result == {"id": "1"}


@patch("app.services.orders.supabase")
def test_get_order_by_id_failure(mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.\
        execute.side_effect = Exception("Order not found")

    with pytest.raises(Exception) as excinfo:
        get_order_by_id("999")

    assert str(excinfo.value) == "Order not found"


@patch("app.services.orders.supabase")
def test_get_orders_by_user_success(mock_supabase):
    mock_execute = MagicMock()
    mock_execute.execute.return_value = [{"id": "1"}]

    mock_supabase.table.return_value.select.return_value.eq.return_value = \
        mock_execute

    result = get_orders_by_user("user_123")

    assert len(result) == 1


@patch("app.services.orders.supabase")
def test_get_orders_by_user_failure(mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.\
        execute.side_effect = Exception("User not found")

    with pytest.raises(Exception) as excinfo:
        get_orders_by_user("user_999")

    assert str(excinfo.value) == "User not found"
