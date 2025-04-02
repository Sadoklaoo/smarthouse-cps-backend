import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db
from app.models.base import Base
from app.models.user import User
from app.core.security import create_access_token
import uuid
from fastapi.testclient import TestClient

# Use an asynchronous PostgreSQL database URL
TEST_DATABASE_URL = "postgresql+asyncpg://testuser:testpassword@test_db:5433/test_db"

# Create an async engine and sessionmaker
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

# Override the database dependency to use async session
async def override_get_db():
    async with TestingSessionLocal() as db:
        yield db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
async def test_db():
    """Set up and tear down the test database."""
    # Create tables for the test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = TestingSessionLocal()
    yield db
    await db.close()
    # Drop tables after the test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def test_user(test_db):
    """Create a test user."""
    user = User(id=uuid.uuid4(), username="testuser", email="test@example.com")
    test_db.add(user)
    await test_db.commit()
    return user

@pytest.fixture(scope="function")
async def auth_headers(test_user):
    """Generate authentication headers for the test user."""
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}

# Make sure your tests are async as well
@pytest.mark.asyncio
async def test_create_device(test_db, auth_headers):
    """Test creating a device via API."""
    response = client.post("/devices/", json={
        "device_name": "Smart Light",
        "device_type": "light",
        "status": True
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["device_name"] == "Smart Light"
