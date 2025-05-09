import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from app.main import app  # Import FastAPI app instance
from app.schemas.sensor import SensorCreate, SensorRead
from app.services.sensor_service import create_sensor, get_sensor_by_id, get_all_sensors, get_sensors_by_device_id, \
    delete_sensor

# Create TestClient to interact with FastAPI
client = TestClient(app)

# Sample data for testing
SENSOR_DATA = {
    "name": "Temperature Sensor",
    "type": "temperature",
    "device_id": "device_123",
    "location": "Living Room",
    "unit": "Celsius",
    "is_active": True,
    "registered_at": "2025-05-01T00:00:00Z"
}


# Test for creating a sensor (POST /sensors/)
@pytest.mark.asyncio
async def test_register_sensor():
    sensor_data = SENSOR_DATA

    # Mock the create_sensor function
    with patch('app.services.sensor_service.create_sensor',
               AsyncMock(return_value=MagicMock(id="sensor_123", **sensor_data))):
        response = client.post("/sensors/", json=sensor_data)

        # Ensure the response status code is 201 Created
        assert response.status_code == 201

        # Check the sensor data in the response
        response_json = response.json()
        assert response_json['name'] == sensor_data['name']
        assert response_json['type'] == sensor_data['type']
        assert response_json['device_id'] == sensor_data['device_id']
        assert response_json['location'] == sensor_data['location']
        assert response_json['unit'] == sensor_data['unit']
        assert response_json['is_active'] == sensor_data['is_active']


# Test for getting all sensors (GET /sensors/)
@pytest.mark.asyncio
async def test_get_all_sensors():
    mock_sensors = [MagicMock(id="sensor_123", **SENSOR_DATA)]

    # Mock the get_all_sensors function to return the mock sensors
    with patch('app.services.sensor_service.get_all_sensors', AsyncMock(return_value=mock_sensors)):
        response = client.get("/sensors/")

        # Ensure the response status code is 200 OK
        assert response.status_code == 200

        # Check the sensor data in the response
        response_json = response.json()
        assert len(response_json) == 1  # Check there is one sensor
        assert response_json[0]['name'] == SENSOR_DATA['name']


# Test for getting a sensor by ID (GET /sensors/{sensor_id})
@pytest.mark.asyncio
async def test_get_sensor_by_id():
    mock_sensor = MagicMock(id="sensor_123", **SENSOR_DATA)

    # Mock the get_sensor_by_id function to return the mock sensor
    with patch('app.services.sensor_service.get_sensor_by_id', AsyncMock(return_value=mock_sensor)):
        response = client.get(f"/sensors/{mock_sensor.id}")

        # Ensure the response status code is 200 OK
        assert response.status_code == 200

        # Check the sensor data in the response
        response_json = response.json()
        assert response_json['name'] == SENSOR_DATA['name']
        assert response_json['device_id'] == SENSOR_DATA['device_id']


# Test for getting sensors by device ID (GET /sensors/device/{device_id})
@pytest.mark.asyncio
async def test_get_sensors_by_device():
    mock_sensor = MagicMock(id="sensor_123", **SENSOR_DATA)

    # Mock the get_sensors_by_device_id function to return the mock sensor
    with patch('app.services.sensor_service.get_sensors_by_device_id', AsyncMock(return_value=[mock_sensor])):
        response = client.get(f"/sensors/device/{SENSOR_DATA['device_id']}")

        # Ensure the response status code is 200 OK
        assert response.status_code == 200

        # Check the sensor data in the response
        response_json = response.json()
        assert len(response_json) == 1  # Check there is one sensor
        assert response_json[0]['device_id'] == SENSOR_DATA['device_id']


# Test for getting sensors by user ID (GET /sensors/user/{user_id})
@pytest.mark.asyncio
async def test_get_sensors_by_user():
    mock_sensor = MagicMock(id="sensor_123", **SENSOR_DATA)

    # Mock the get_sensors_by_user function to return the mock sensor
    with patch('app.services.sensor_service.get_sensors_by_user', AsyncMock(return_value=[mock_sensor])):
        response = client.get(f"/sensors/user/{SENSOR_DATA['device_id']}")

        # Ensure the response status code is 200 OK
        assert response.status_code == 200

        # Check the sensor data in the response
        response_json = response.json()
        assert len(response_json) == 1  # Check there is one sensor


# Test for deleting a sensor (DELETE /sensors/{sensor_id})
@pytest.mark.asyncio
async def test_delete_sensor():
    mock_sensor = MagicMock(id="sensor_123", **SENSOR_DATA)

    # Mock the delete_sensor function to return True
    with patch('app.services.sensor_service.delete_sensor', AsyncMock(return_value=True)):
        response = client.delete(f"/sensors/{mock_sensor.id}")

        # Ensure the response status code is 204 No Content
        assert response.status_code == 204


# Test for deleting a non-existent sensor (DELETE /sensors/{sensor_id})
@pytest.mark.asyncio
async def test_delete_sensor_not_found():
    # Mock the delete_sensor function to return False
    with patch('app.services.sensor_service.delete_sensor', AsyncMock(return_value=False)):
        response = client.delete("/sensors/non_existent_sensor_id")

        # Ensure the response status code is 404 Not Found
        assert response.status_code == 404
        assert response.json()['detail'] == "Sensor not found"
