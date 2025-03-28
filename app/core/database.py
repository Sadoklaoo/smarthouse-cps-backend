from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from app.models.base import Base

# Create async engine
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

# Create session factory
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



# Dependency for database session
async def get_db():
    async with async_session() as session:
        yield session


# Test function to check database connection
async def test_database_connection():
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(1))
            return result.scalar()  # This should return 1 if the query is successful


# Create all tables in the database
async def create_tables():
    async with engine.begin() as conn:
        # Create all tables based on Base
        await conn.run_sync(Base.metadata.create_all)