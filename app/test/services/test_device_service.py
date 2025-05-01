import pytest
from unittest.mock import patch, MagicMock
from unittest.mock import AsyncMock
from app.services.device_service import create_device, get_device_by_id, update_device, delete_device
from app.schemas.device import DeviceCreate, DeviceUpdate

# Ensure that you're using valid MongoDB ObjectIds (24-character hex strings)
VALID_OBJECT_ID = "60b6a6fa5f3c1f5f56e8391b"

# Test for creating a device
@pytest.mark.asyncio
async def test_create_device():
    device_data = DeviceCreate(name="Device 1", user_id="user_123", type="smart")
    mock_device = MagicMock()

    # Setting return values for mocked attributes
    mock_device.name = "Device 1"
    mock_device.type = "smart"
    mock_device.insert = AsyncMock()  # Mock async insert method

    # Patch the 'Device' class to return our mock device
    with patch('app.services.device_service.Device', return_value=mock_device):
        device = await create_device(device_data)

        # Check if 'insert' was called and that the name and type are correctly assigned
        mock_device.insert.assert_called_once()
        assert device.name == "Device 1"
        assert device.type == "smart"


# Test for getting a device by ID
@pytest.mark.asyncio
async def test_get_device_by_id():
    mock_device = MagicMock()
    mock_device.id = VALID_OBJECT_ID  # Use valid ObjectId

    # Patch the 'Device.get' method to return the mock device
    with patch('app.services.device_service.Device.get', return_value=mock_device):
        device = await get_device_by_id(VALID_OBJECT_ID)  # Use valid ObjectId
        assert device.id == VALID_OBJECT_ID


# Test for updating a device
@pytest.mark.asyncio
async def test_update_device():
    device_data = DeviceUpdate(name="Updated Device")
    mock_device = MagicMock()
    mock_device.id = "device_123"
    mock_device.name = "Old Device"
    mock_device.save = AsyncMock()  # Mock async save method

    # Patch the 'get_device_by_id' service to return the mock device
    with patch('app.services.device_service.get_device_by_id', return_value=mock_device):
        updated_device = await update_device("device_123", device_data)

        # Ensure that the name is updated and the save method is called once
        assert updated_device.name == "Updated Device"
        mock_device.save.assert_called_once()


# Test for deleting a device
@pytest.mark.asyncio
async def test_delete_device():
    mock_device = MagicMock()
    mock_device.id = "device_123"
    mock_device.delete = AsyncMock()  # Mock async delete method

    # Patch the 'get_device_by_id' service to return the mock device
    with patch('app.services.device_service.get_device_by_id', return_value=mock_device):
        result = await delete_device("device_123")
        assert result is True
        mock_device.delete.assert_called_once()  # Verify delete was called once
