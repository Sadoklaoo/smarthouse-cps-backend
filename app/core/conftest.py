import os
import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.models.base import Base

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# Create async database engine
engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Initialize the database before running tests
@pytest.fixture(scope="session")
def event_loop():
    """Create a new event loop for testing."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Create and drop tables for testing."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def test_db():
    """Provide a fresh database session for each test."""
    async with TestingSessionLocal() as session:
        yield session