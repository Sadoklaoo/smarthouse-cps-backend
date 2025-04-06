import time
import asyncpg
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
from httpx import AsyncClient  # Use AsyncClient from httpx instead of TestClient

# Use an asynchronous PostgreSQL database URL
TEST_DATABASE_URL = "postgresql+asyncpg://testuser:testpassword@test_db:5432/test_db"

# Create an async engine and sessionmaker
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

# Override the database dependency to use async session
async def override_get_db():
    async with TestingSessionLocal() as db:
        yield db

app.dependency_overrides[get_db] = override_get_db

# Use AsyncClient from httpx for async requests
@pytest.fixture(scope="function")
async def client(test_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

async def wait_for_postgres():
    import asyncpg
    retries = 10
    while retries > 0:
        try:
            conn = await asyncpg.connect("postgresql://testuser:testpassword@test_db:5432/test_db")
            await conn.close()
            return
        except Exception as e:
            print("Waiting for PostgreSQL...", e)
            retries -= 1
            await asyncio.sleep(1)
    raise RuntimeError("PostgreSQL not available after retries.")


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_for_postgres())
    return loop


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
    user = User(id=uuid.uuid4(), username="testuser", email="test@example.com", hashed_password="testpassword")
    test_db.add(user)
    await test_db.commit()
    return user

@pytest.fixture(scope="function")
async def auth_headers(test_user):
    """Generate authentication headers for the test user."""
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}

# Test function updated for async calls
@pytest.mark.asyncio
async def test_create_device(client, test_db, auth_headers):
    """Test creating a device via API."""
    response = await client.post("/devices/", json={
        "device_name": "Smart Light",
        "device_type": "light",
        "status": True
    }, headers=auth_headers)

    assert response.status_code == 201
    assert response.json()["device_name"] == "Smart Light"
