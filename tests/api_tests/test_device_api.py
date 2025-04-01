import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db
from app.models.base import Base
from app.models.user import User
from app.core.security import create_access_token
import uuid

# Create a test database
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override the database dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the test client
client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    """Set up and tear down the test database."""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def test_user(test_db):
    """Create a test user."""
    user = User(id=uuid.uuid4(), username="testuser", email="test@example.com")
    test_db.add(user)
    test_db.commit()
    return user

@pytest.fixture(scope="function")
def auth_headers(test_user):
    """Generate authentication headers for the test user."""
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}

def test_create_device(test_db, auth_headers):
    """Test creating a device via API."""
    response = client.post("/devices/", json={
        "device_name": "Smart Light",
        "device_type": "light",
        "status": True
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["device_name"] == "Smart Light"

def test_get_devices(test_db, auth_headers):
    """Test retrieving devices via API."""
    client.post("/devices/", json={
        "device_name": "Test Device",
        "device_type": "thermostat",
        "status": False
    }, headers=auth_headers)
    response = client.get("/devices/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_device_not_found(auth_headers):
    """Test retrieving a non-existent device."""
    response = client.get(f"/devices/{uuid.uuid4()}", headers=auth_headers)
    assert response.status_code == 404

def test_update_device(test_db, auth_headers):
    """Test updating a device status via API."""
    create_response = client.post("/devices/", json={
        "device_name": "Smart Switch",
        "device_type": "light",
        "status": False
    }, headers=auth_headers)
    device_id = create_response.json()["id"]
    update_response = client.patch(f"/devices/{device_id}", json={"status": True}, headers=auth_headers)
    assert update_response.status_code == 200
    assert update_response.json()["status"] is True

def test_delete_device(test_db, auth_headers):
    """Test deleting a device via API."""
    create_response = client.post("/devices/", json={
        "device_name": "Smart Sensor",
        "device_type": "sensor",
        "status": True
    }, headers=auth_headers)
    device_id = create_response.json()["id"]
    delete_response = client.delete(f"/devices/{device_id}", headers=auth_headers)
    assert delete_response.status_code == 204
