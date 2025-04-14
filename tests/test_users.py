import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_user_workflow():
    transport = ASGITransport(app=app)  # Use ASGITransport to connect to the FastAPI app
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create a new user
        create_response = await client.post(
            "/api/users/",
            json={
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "password123",
                "role": "admin"
            }
        )
        assert create_response.status_code == 200
        user_data = create_response.json()
        assert user_data["username"] == "testuser"

        # Login with the created user
        login_response = await client.post(
            "/api/users/login",
            data={"username": "testuser", "password": "password123"}
        )
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data

        # Access protected route with the token
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        users_response = await client.get("/api/users/", headers=headers)
        assert users_response.status_code == 200
        users_data = users_response.json()
        assert isinstance(users_data, list)