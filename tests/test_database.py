import pytest
from sqlalchemy import select, text
from app.core.database import async_session
from app.models.user import User, UserRole


@pytest.mark.asyncio
async def test_database_connection():
    async with async_session() as session:
        result = await session.execute(select(1))
        assert result.scalar() == 1


@pytest.mark.asyncio
async def test_create_user():
    async with async_session() as session:
        # Create a new user
        new_user = User(
            username="john_doe", email="john@example.com", password="password123"
        )
        session.add(new_user)
        await session.commit()

        # Retrieve the user from the database
        result = await session.execute(select(User).filter_by(username="john_doe"))
        user = result.scalars().first()

        # Assertions
        assert user is not None
        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.role == UserRole.RESIDENT
        assert (
            user.password != "password123"
        )  # Make sure the password is hashed in real scenarios


@pytest.mark.asyncio
async def test_get_user_by_id():
    async with async_session() as session:
        # Create a new user
        new_user = User(
            username="alice_smith", email="alice@example.com", password="password123"
        )
        session.add(new_user)
        await session.commit()

        # Retrieve the user by ID
        result = await session.execute(select(User).filter_by(username="alice_smith"))
        user = result.scalars().first()

        assert user is not None
        assert user.id is not None

        # Fetch the user by ID
        user_by_id = await session.get(User, user.id)
        assert user_by_id is not None
        assert user_by_id.id == user.id


@pytest.mark.asyncio
async def test_update_user():
    async with async_session() as session:
        # Create a new user
        new_user = User(
            username="bob_jones", email="bob@example.com", password="password123"
        )
        session.add(new_user)
        await session.commit()

        # Retrieve the user from the database
        result = await session.execute(select(User).filter_by(username="bob_jones"))
        user = result.scalars().first()

        # Update user details
        user.username = "bob_updated"
        await session.commit()

        # Retrieve the updated user
        result = await session.execute(select(User).filter_by(id=user.id))
        updated_user = result.scalars().first()

        # Assertions
        assert updated_user is not None
        assert updated_user.username == "bob_updated"
        assert updated_user.email == "bob@example.com"


@pytest.mark.asyncio
async def test_delete_user():
    async with async_session() as session:
        # Create a new user
        new_user = User(
            username="charlie_brown",
            email="charlie@example.com",
            password="password123",
        )
        session.add(new_user)
        await session.commit()

        # Retrieve the user from the database
        result = await session.execute(select(User).filter_by(username="charlie_brown"))
        user = result.scalars().first()

        # Delete the user
        await session.delete(user)
        await session.commit()

        # Verify that the user has been deleted
        result = await session.execute(select(User).filter_by(id=user.id))
        deleted_user = result.scalars().first()
        assert deleted_user is None
