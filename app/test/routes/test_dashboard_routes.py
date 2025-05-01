import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app  # Import your FastAPI app

client = TestClient(app)

# Mock data for testing with valid ObjectId (using 24-character hex string format)
mock_user_data = {
    "_id": "60b6a6fa5f3c1f5f56e8391b",  # Example valid ObjectId
    "name": "John Doe",
    "email": "johndoe@example.com"
}

mock_device_data = [
    {
        "_id": "60b6a6fa5f3c1f5f56e8391c",  # Another valid ObjectId
        "name": "Smart Light",
        "type": "light",
        "location": "Living Room",
        "is_active": True
    },
    {
        "_id": "60b6a6fa5f3c1f5f56e8391d",  # Another valid ObjectId
        "name": "Smart Thermostat",
        "type": "thermostat",
        "location": "Bedroom",
        "is_active": True
    }
]

mock_sensor_data = [
    {
        "_id": "60b6a6fa5f3c1f5f56e8391e",  # Another valid ObjectId
        "name": "Temperature Sensor",
        "type": "temperature",
        "unit": "°C",
        "is_active": True
    },
    {
        "_id": "60b6a6fa5f3c1f5f56e8391f",  # Another valid ObjectId
        "name": "Humidity Sensor",
        "type": "humidity",
        "unit": "%",
        "is_active": True
    }
]

# Test: Get User Dashboard
@pytest.mark.asyncio
async def test_get_user_dashboard():
    # Mock the external service calls to return mock data with valid ObjectIds
    with patch("app.services.user_service.get_user_by_id", return_value=mock_user_data):
        with patch("app.services.device_service.get_devices_by_user", return_value=mock_device_data):
            with patch("app.services.sensor_service.get_sensors_by_device_id", return_value=mock_sensor_data):

                # Make the request to the /dashboard/{user_id} endpoint
                response = client.get("/api/dashboard/60b6a6fa5f3c1f5f56e8391b")  # Use valid ObjectId here
                assert response.status_code == 200

                # Parse the response JSON
                dashboard_data = response.json()

                # Check if the dashboard response contains the expected data
                assert dashboard_data["user_id"] == "60b6a6fa5f3c1f5f56e8391b"
                assert len(dashboard_data["devices"]) == 2
                assert dashboard_data["devices"][0]["id"] == "60b6a6fa5f3c1f5f56e8391c"
                assert dashboard_data["devices"][1]["id"] == "60b6a6fa5f3c1f5f56e8391d"

                # Check that sensor data is present under each device
                assert len(dashboard_data["devices"][0]["sensors"]) == 2
                assert dashboard_data["devices"][0]["sensors"][0]["id"] == "60b6a6fa5f3c1f5f56e8391e"
                assert dashboard_data["devices"][0]["sensors"][1]["id"] == "60b6a6fa5f3c1f5f56e8391f"

                # Check the sensor details
                assert dashboard_data["devices"][0]["sensors"][0]["name"] == "Temperature Sensor"
                assert dashboard_data["devices"][0]["sensors"][1]["name"] == "Humidity Sensor"

# Test: User Not Found
@pytest.mark.asyncio
async def test_get_user_dashboard_user_not_found():
    # Mock the get_user_by_id service to return None (user not found)
    with patch("app.services.user_service.get_user_by_id", return_value=None):
        response = client.get("/api/dashboard/60b6a6fa5f3c1f5f56e8392a")  # Non-existing user ObjectId
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

# Test: Internal Server Error Handling
@pytest.mark.asyncio
async def test_get_user_dashboard_internal_error():
    # Mock the get_user_by_id service to raise an exception
    with patch("app.services.user_service.get_user_by_id", side_effect=Exception("Internal server error")):
        response = client.get("/api/dashboard/60b6a6fa5f3c1f5f56e8391b")
        assert response.status_code == 500
        assert response.json() == {"detail": "Dashboard error: Internal server error"}
