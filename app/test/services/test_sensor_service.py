import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.services.sensor_service import (
    create_sensor,
    get_sensor_by_id,
    get_all_sensors,
    get_sensors_by_device_id,
    get_sensors_by_user,
    delete_sensor,
)
from app.schemas.sensor import SensorCreate, SensorUpdate


# Mocking ObjectIds for testing
VALID_OBJECT_ID = "60b6a6fa5f3c1f5f56e8391b"  # Valid MongoDB ObjectId


# Test for creating a sensor
@pytest.mark.asyncio
async def test_create_sensor():
    sensor_data = SensorCreate(name="Temperature Sensor", device_id=VALID_OBJECT_ID, type="temperature")
    mock_sensor = MagicMock()
    mock_sensor.name = "Temperature Sensor"
    mock_sensor.device_id = VALID_OBJECT_ID
    mock_sensor.insert = AsyncMock()

    # Mocking the device check and insert
    mock_device = MagicMock()
    mock_device.id = VALID_OBJECT_ID

    with patch('app.services.sensor_service.get_device_by_id', return_value=mock_device):
        with patch('app.services.sensor_service.Sensor', return_value=mock_sensor):
            sensor = await create_sensor(sensor_data)

            # Ensure insert was called and sensor is created
            mock_sensor.insert.assert_called_once()
            assert sensor.name == "Temperature Sensor"
            assert sensor.device_id == VALID_OBJECT_ID


# Test for getting a sensor by ID
@pytest.mark.asyncio
async def test_get_sensor_by_id():
    mock_sensor = MagicMock()
    mock_sensor.id = VALID_OBJECT_ID

    with patch('app.services.sensor_service.Sensor.get', return_value=mock_sensor):
        sensor = await get_sensor_by_id(VALID_OBJECT_ID)
        assert sensor.id == VALID_OBJECT_ID


# Test for getting all sensors
@pytest.mark.asyncio
async def test_get_all_sensors():
    mock_sensor_1 = MagicMock()
    mock_sensor_1.id = VALID_OBJECT_ID
    mock_sensor_2 = MagicMock()
    mock_sensor_2.id = "60b6a6fa5f3c1f5f56e8391c"  # Another valid ObjectId

    # Mocking the return value of find_all() to simulate a list-like object with `.to_list()`
    with patch('app.services.sensor_service.Sensor.find_all', return_value=[mock_sensor_1, mock_sensor_2]):
        sensors = await get_all_sensors()
        assert len(sensors) == 2
        assert sensors[0].id == VALID_OBJECT_ID
        assert sensors[1].id == "60b6a6fa5f3c1f5f56e8391c"


# Test for getting sensors by device ID
@pytest.mark.asyncio
async def test_get_sensors_by_device_id():
    mock_sensor = MagicMock()
    mock_sensor.id = VALID_OBJECT_ID

    # Mock the find() method to return a list
    with patch('app.services.sensor_service.Sensor.find', return_value=[mock_sensor]):
        sensors = await get_sensors_by_device_id(VALID_OBJECT_ID)
        assert len(sensors) == 1
        assert sensors[0].id == VALID_OBJECT_ID


# Test for getting sensors by user ID
@pytest.mark.asyncio
async def test_get_sensors_by_user():
    mock_device = MagicMock()
    mock_device.id = VALID_OBJECT_ID

    mock_sensor = MagicMock()
    mock_sensor.id = VALID_OBJECT_ID

    # Mock the get_devices_by_user and Sensor.find_many methods
    with patch('app.services.sensor_service.get_devices_by_user', return_value=[mock_device]):
        with patch('app.services.sensor_service.Sensor.find_many', return_value=[mock_sensor]):
            sensors = await get_sensors_by_user("60f5c4a1b4c32f1b5c1d34c5")  # Valid ObjectId for user
            assert len(sensors) == 1
            assert sensors[0].id == VALID_OBJECT_ID


# Test for deleting a sensor
@pytest.mark.asyncio
async def test_delete_sensor():
    mock_sensor = MagicMock()
    mock_sensor.id = VALID_OBJECT_ID
    mock_sensor.delete = AsyncMock()

    with patch('app.services.sensor_service.get_sensor_by_id', return_value=mock_sensor):
        result = await delete_sensor(VALID_OBJECT_ID)
        assert result is True
        mock_sensor.delete.assert_called_once()
