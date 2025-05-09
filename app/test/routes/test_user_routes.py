import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from app.main import app  # Import the FastAPI app instance
from app.schemas.user import UserCreate, UserUpdate, UserRead
from fastapi import HTTPException

# Create a TestClient to interact with the FastAPI app
client = TestClient(app)

# Sample data for testing
USER_DATA = {
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
}


# Test for user registration (POST /users/)
@pytest.mark.asyncio
async def test_register_user():
    user_data = USER_DATA
    # Mock the get_user_by_email function to return None (user does not exist)
    with patch('app.services.user_service.get_user_by_email', AsyncMock(return_value=None)), \
            patch('app.services.user_service.create_user',
                  AsyncMock(return_value=MagicMock(id="user_123", **user_data))):
        response = client.post("/users/", json=user_data)

        # Ensure the response status code is 201 Created
        assert response.status_code == 201

        # Check that the returned data matches what we expect
        assert response.json()['email'] == user_data['email']
        assert response.json()['full_name'] == user_data['full_name']


# Test for user registration when user already exists (POST /users/)
@pytest.mark.asyncio
async def test_register_user_already_exists():
    user_data = USER_DATA
    # Mock the get_user_by_email function to return a user (already exists)
    with patch('app.services.user_service.get_user_by_email',
               AsyncMock(return_value=MagicMock(id="user_123", **user_data))):
        response = client.post("/users/", json=user_data)

        # Ensure the response status code is 400 Bad Request (user already exists)
        assert response.status_code == 400
        assert response.json()['detail'] == "User with this email already exists."


# Test for getting a user by ID (GET /users/{user_id})
@pytest.mark.asyncio
async def test_get_user_by_id():
    user_data = USER_DATA
    # Mock the get_user_by_id function to return a user
    with patch('app.services.user_service.get_user_by_id',
               AsyncMock(return_value=MagicMock(id="user_123", **user_data))):
        response = client.get("/users/user_123")

        # Ensure the response status code is 200 OK
        assert response.status_code == 200

        # Check that the returned data matches the expected user data
        assert response.json()['email'] == user_data['email']
        assert response.json()['full_name'] == user_data['full_name']


# Test for getting a user by ID when the user does not exist (GET /users/{user_id})
@pytest.mark.asyncio
async def test_get_user_by_id_not_found():
    # Mock the get_user_by_id function to return None (user not found)
    with patch('app.services.user_service.get_user_by_id', AsyncMock(return_value=None)):
        response = client.get("/users/non_existing_user_id")

        # Ensure the response is 404 Not Found and the correct message is returned
        assert response.status_code == 404
        assert response.json()['detail'] == "User not found."


# Test for updating a user (PUT /users/{user_id})
@pytest.mark.asyncio
async def test_update_user():
    user_data = USER_DATA
    update_data = UserUpdate(full_name="Updated User")

    # Mock the get_user_by_id function to return the mock user
    with patch('app.services.user_service.get_user_by_id',
               AsyncMock(return_value=MagicMock(id="user_123", **user_data))), \
            patch('app.services.user_service.update_user',
                  AsyncMock(return_value=MagicMock(id="user_123", **user_data, full_name="Updated User"))):
        response = client.put("/users/user_123", json=update_data.dict())

        # Ensure the response status code is 200 OK
        assert response.status_code == 200

        # Check that the full name was updated
        assert response.json()['full_name'] == "Updated User"


# Test for deleting a user (DELETE /users/{user_id})
@pytest.mark.asyncio
async def test_delete_user():
    # Mock the delete_user function to return True (user deleted successfully)
    with patch('app.services.user_service.delete_user', AsyncMock(return_value=True)):
        response = client.delete("/users/user_123")

        # Ensure the response status code is 204 No Content (no body in response)
        assert response.status_code == 204


# Test for deleting a user when the user is not found (DELETE /users/{user_id})
@pytest.mark.asyncio
async def test_delete_user_not_found():
    # Mock the delete_user function to return False (user not found)
    with patch('app.services.user_service.delete_user', AsyncMock(return_value=False)):
        response = client.delete("/users/non_existing_user_id")

        # Ensure the response status code is 404 Not Found
        assert response.status_code == 404
        assert response.json()['detail'] == "User not found"

