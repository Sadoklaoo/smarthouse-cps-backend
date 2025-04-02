import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base

@pytest.fixture(scope="session")
async def test_db():
    # Test database URL pointing to the test container
    DATABASE_URL = "postgresql+asyncpg://testuser:testpassword@test_db:5433/test_db"
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)

    # Create all tables in the test database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine  # This will be used by the tests

    # Cleanup after the tests are done
    await engine.dispose()
