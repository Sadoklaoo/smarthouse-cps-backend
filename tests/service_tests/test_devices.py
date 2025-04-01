import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.device import Device
from app.models.user import User
from app.services.device_service import (
    create_device_service,
    get_devices_service,
    get_device_service,
    update_device_status_service,
    delete_device_service,
)
from app.schemas.device import DeviceCreate, DeviceUpdate
import uuid

# Create an in-memory SQLite database for testing
test_engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="function")
def db_session():
    """Creates a new database session for each test."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def test_user(db_session):
    """Creates a test user."""
    user = User(id=uuid.uuid4(), username="testuser", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture(scope="function")
def test_device(test_user, db_session):
    """Creates a test device."""
    device_data = DeviceCreate(device_name="Test Device", device_type="light", status=True)
    return create_device_service(device_data, db_session, test_user)

def test_create_device(db_session, test_user):
    """Test creating a new device."""
    device_data = DeviceCreate(device_name="New Device", device_type="thermostat", status=False)
    device = create_device_service(device_data, db_session, test_user)
    assert device.device_name == "New Device"
    assert device.device_type.value == "thermostat"
    assert device.status is False

def test_get_devices(db_session, test_user, test_device):
    """Test retrieving all devices for a user."""
    devices = get_devices_service(db_session, test_user)
    assert len(devices) == 1
    assert devices[0].device_name == "Test Device"

def test_get_device(db_session, test_user, test_device):
    """Test retrieving a specific device."""
    device = get_device_service(test_device.id, db_session, test_user)
    assert device.id == test_device.id

def test_update_device_status(db_session, test_user, test_device):
    """Test updating a device's status."""
    update_data = DeviceUpdate(status=False)
    updated_device = update_device_status_service(test_device.id, update_data, db_session, test_user)
    assert updated_device.status is False

def test_delete_device(db_session, test_user, test_device):
    """Test deleting a device."""
    delete_device_service(test_device.id, db_session, test_user)
    devices = get_devices_service(db_session, test_user)
    assert len(devices) == 0

def test_get_nonexistent_device(db_session, test_user):
    """Test retrieving a device that does not exist."""
    with pytest.raises(Exception):
        get_device_service(uuid.uuid4(), db_session, test_user)

def test_update_nonexistent_device(db_session, test_user):
    """Test updating a device that does not exist."""
    with pytest.raises(Exception):
        update_device_status_service(uuid.uuid4(), DeviceUpdate(status=True), db_session, test_user)

def test_delete_nonexistent_device(db_session, test_user):
    """Test deleting a device that does not exist."""
    with pytest.raises(Exception):
        delete_device_service(uuid.uuid4(), db_session, test_user)
