import pytest
from unittest.mock import MagicMock
from app.services.device_service import (
    create_device_service,
    get_devices_service,
    get_device_service,
    update_device_status_service,
    delete_device_service
)
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceTypeEnum
from fastapi import HTTPException
import uuid


@pytest.fixture
def mock_db():
    """Fixture to mock the database session."""
    return MagicMock()


@pytest.fixture
def device_create_data():
    """Fixture to provide device creation data."""
    return DeviceCreate(
        device_name="Smart Light", 
        device_type=DeviceTypeEnum.LIGHT, 
        status=True
    )


@pytest.fixture
def device_update_data():
    """Fixture to provide device update data."""
    return DeviceUpdate(status=False)


# Test Create Device Service
def test_create_device_service(mock_db, device_create_data, caplog):
    """Test the creation of a device."""

    # Mock the behavior of the database session
    mock_device = MagicMock(spec=Device)
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=mock_device)

    # Run the service method
    with caplog.at_level('INFO'):
        new_device = create_device_service(device_create_data, mock_db)

    # Assert the expected results
    assert new_device.device_name == "Smart Light"
    assert new_device.device_type == DeviceTypeEnum.LIGHT
    assert new_device.status is True
    mock_db.add.assert_called_once_with(new_device)
    mock_db.commit.assert_called_once()

    # Check the logs
    assert "Creating new device: Smart Light" in caplog.text
    assert "Device created successfully with ID:" in caplog.text


# Test Get Devices Service
def test_get_devices_service(mock_db, caplog):
    """Test retrieving all devices."""

    # Mock the behavior of the database session
    mock_devices = [MagicMock(spec=Device), MagicMock(spec=Device)]
    mock_db.query().all.return_value = mock_devices

    # Run the service method
    with caplog.at_level('INFO'):
        devices = get_devices_service(mock_db)

    # Assert the expected results
    assert len(devices) == 2
    mock_db.query().all.assert_called_once()

    # Check the logs
    assert "Fetching all devices" in caplog.text


# Test Get Device Service
def test_get_device_service(mock_db, caplog):
    """Test retrieving a single device by ID."""

    device_id = uuid.uuid4()
    mock_device = MagicMock(spec=Device)
    mock_db.query().filter().first.return_value = mock_device

    # Run the service method
    with caplog.at_level('INFO'):
        device = get_device_service(device_id, mock_db)

    # Assert the expected results
    assert device == mock_device
    mock_db.query().filter().first.assert_called_once()

    # Check the logs
    assert f"Fetching device with ID: {device_id}" in caplog.text


# Test Get Device Service (Device Not Found)
def test_get_device_service_not_found(mock_db, caplog):
    """Test retrieving a non-existing device by ID."""

    device_id = uuid.uuid4()
    mock_db.query().filter().first.return_value = None

    # Run the service method and expect an exception
    with caplog.at_level('WARNING'):
        with pytest.raises(HTTPException):
            get_device_service(device_id, mock_db)

    # Check the logs
    assert f"Device not found: {device_id}" in caplog.text


# Test Update Device Status Service
def test_update_device_status_service(mock_db, device_update_data, caplog):
    """Test updating a device's status."""

    device_id = uuid.uuid4()
    mock_device = MagicMock(spec=Device)
    mock_db.query().filter().first.return_value = mock_device

    # Run the service method
    with caplog.at_level('INFO'):
        updated_device = update_device_status_service(device_id, device_update_data, mock_db)

    # Assert the expected results
    assert updated_device.status is False
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    # Check the logs
    assert f"Updating device status for ID: {device_id}" in caplog.text
    assert f"Device updated successfully: {device_id}" in caplog.text


# Test Update Device Status Service (Device Not Found)
def test_update_device_status_service_not_found(mock_db, device_update_data, caplog):
    """Test updating a device that does not exist."""

    device_id = uuid.uuid4()
    mock_db.query().filter().first.return_value = None

    # Run the service method and expect an exception
    with caplog.at_level('WARNING'):
        with pytest.raises(HTTPException):
            update_device_status_service(device_id, device_update_data, mock_db)

    # Check the logs
    assert f"Device not found for update: {device_id}" in caplog.text


# Test Delete Device Service
def test_delete_device_service(mock_db, caplog):
    """Test deleting a device by ID."""

    device_id = uuid.uuid4()
    mock_device = MagicMock(spec=Device)
    mock_db.query().filter().first.return_value = mock_device

    # Run the service method
    with caplog.at_level('INFO'):
        delete_device_service(device_id, mock_db)

    # Assert the expected results
    mock_db.delete.assert_called_once_with(mock_device)
    mock_db.commit.assert_called_once()

    # Check the logs
    assert f"Deleting device with ID: {device_id}" in caplog.text
    assert f"Device deleted successfully: {device_id}" in caplog.text


# Test Delete Device Service (Device Not Found)
def test_delete_device_service_not_found(mock_db, caplog):
    """Test deleting a device that does not exist."""

    device_id = uuid.uuid4()
    mock_db.query().filter().first.return_value = None

    # Run the service method and expect an exception
    with caplog.at_level('WARNING'):
        with pytest.raises(HTTPException):
            delete_device_service(device_id, mock_db)

    # Check the logs
    assert f"Device not found for deletion: {device_id}" in caplog.text
