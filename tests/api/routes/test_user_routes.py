import pytest
from httpx import AsyncClient
from fastapi import status
from unittest.mock import patch, MagicMock
from app.main import app  # Assuming your FastAPI app instance is here
from app.schemas.user import UserCreate, UserRead, UserUpdate
from datetime import datetime, timezone
from bson import ObjectId

@pytest.fixture
def mock_user_service():
    with patch("app.api.routes.user_routes.create_user") as mock_create, \
         patch("app.api.routes.user_routes.get_user_by_email") as mock_get_by_email, \
         patch("app.api.routes.user_routes.get_user_by_id") as mock_get_by_id, \
         patch("app.api.routes.user_routes.update_user") as mock_update, \
         patch("app.api.routes.user_routes.delete_user") as mock_delete:
        yield mock_create, mock_get_by_email, mock_get_by_id, mock_update, mock_delete

@pytest.fixture
def user_create_payload():
    return {
        "email": "test@example.com",
        "password": "securepassword123",
        "full_name": "Test User"
    }

@pytest.fixture
def user_update_payload():
    return {
        "full_name": "Test User Updated",
        "is_active": False
    }

@pytest.fixture
def mock_user_doc(user_create_payload):
    return MagicMock(
        id=ObjectId(),
        email=user_create_payload["email"],
        full_name=user_create_payload["full_name"],
        is_active=True, # Default for new user
        created_at=datetime.now(timezone.utc)
        # password/hashed_password is not part of UserRead schema
    )

@pytest.mark.asyncio
async def test_register_user_route(mock_user_service, user_create_payload, mock_user_doc):
    mock_create, mock_get_by_email, _, _, _ = mock_user_service
    mock_get_by_email.return_value = None # No existing user
    mock_create.return_value = mock_user_doc

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/users/", json=user_create_payload)

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["email"] == mock_user_doc.email
    assert response_data["full_name"] == mock_user_doc.full_name
    assert response_data["is_active"] == mock_user_doc.is_active
    assert "id" in response_data
    assert "created_at" in response_data
    mock_get_by_email.assert_called_once_with(user_create_payload["email"])
    mock_create.assert_called_once()
    call_args = mock_create.call_args[0][0]
    assert isinstance(call_args, UserCreate)
    assert call_args.email == user_create_payload["email"]

@pytest.mark.asyncio
async def test_register_user_route_already_exists(mock_user_service, user_create_payload, mock_user_doc):
    _, mock_get_by_email, _, _, _ = mock_user_service
    mock_get_by_email.return_value = mock_user_doc # Simulate user already exists

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/users/", json=user_create_payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User with this email already exists."

@pytest.mark.asyncio
async def test_register_user_route_create_error(mock_user_service, user_create_payload):
    mock_create, mock_get_by_email, _, _, _ = mock_user_service
    mock_get_by_email.return_value = None
    mock_create.side_effect = Exception("DB write error")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/users/", json=user_create_payload)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Error registering user: DB write error" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_user_route(mock_user_service, mock_user_doc):
    _, _, mock_get_by_id, _, _ = mock_user_service
    user_id_str = str(mock_user_doc.id)
    mock_get_by_id.return_value = mock_user_doc

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/api/users/{user_id_str}")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == user_id_str
    assert response_data["email"] == mock_user_doc.email
    mock_get_by_id.assert_called_once_with(user_id_str)

@pytest.mark.asyncio
async def test_get_user_route_not_found(mock_user_service):
    _, _, mock_get_by_id, _, _ = mock_user_service
    user_id_str = str(ObjectId())
    mock_get_by_id.return_value = None

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/api/users/{user_id_str}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found."

@pytest.mark.asyncio
async def test_get_user_route_error(mock_user_service):
    _, _, mock_get_by_id, _, _ = mock_user_service
    user_id_str = str(ObjectId())
    mock_get_by_id.side_effect = Exception("Fetch error")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/api/users/{user_id_str}")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Error fetching user: Fetch error" in response.json()["detail"]

@pytest.mark.asyncio
async def test_update_user_route(mock_user_service, user_update_payload, mock_user_doc):
    _, _, _, mock_update, _ = mock_user_service
    user_id_str = str(mock_user_doc.id)

    updated_user_data = mock_user_doc
    updated_user_data.full_name = user_update_payload["full_name"]
    updated_user_data.is_active = user_update_payload["is_active"]
    mock_update.return_value = updated_user_data

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/api/users/{user_id_str}", json=user_update_payload)

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == user_id_str
    assert response_data["full_name"] == user_update_payload["full_name"]
    assert response_data["is_active"] == user_update_payload["is_active"]
    mock_update.assert_called_once()
    call_args = mock_update.call_args
    assert call_args[0][0] == user_id_str
    assert isinstance(call_args[0][1], UserUpdate)
    assert call_args[0][1].full_name == user_update_payload["full_name"]

@pytest.mark.asyncio
async def test_update_user_route_generic_error(mock_user_service, user_update_payload):
    _, _, _, mock_update, _ = mock_user_service
    user_id_str = str(ObjectId())
    mock_update.side_effect = Exception("Generic update error")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/api/users/{user_id_str}", json=user_update_payload)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Error updating user: Generic update error" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_user_route(mock_user_service):
    _, _, _, _, mock_delete = mock_user_service
    user_id_str = str(ObjectId())
    mock_delete.return_value = True # Simulate successful deletion

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/api/users/{user_id_str}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    mock_delete.assert_called_once_with(user_id_str)

@pytest.mark.asyncio
async def test_delete_user_route_not_found(mock_user_service):
    _, _, _, _, mock_delete = mock_user_service
    user_id_str = str(ObjectId())
    mock_delete.return_value = False # Simulate user not found by service

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/api/users/{user_id_str}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_delete_user_route_error(mock_user_service):
    _, _, _, _, mock_delete = mock_user_service
    user_id_str = str(ObjectId())
    mock_delete.side_effect = Exception("Deletion DB error")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/api/users/{user_id_str}")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Error deleting user: Deletion DB error" in response.json()["detail"]

