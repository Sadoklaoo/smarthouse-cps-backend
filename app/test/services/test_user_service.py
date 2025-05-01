import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    activate_user,
    update_user,
    delete_user,
)
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User

# Mocking valid object IDs
VALID_USER_ID = "60f5c4a1b4c32f1b5c1d34c5"  # Valid ObjectId for user
VALID_EMAIL = "test@example.com"
VALID_PASSWORD = "securepassword123"

# Test for creating a user
@pytest.mark.asyncio
async def test_create_user():
    user_data = UserCreate(email=VALID_EMAIL, full_name="Test User", password=VALID_PASSWORD)
    mock_user = MagicMock()
    mock_user.email = VALID_EMAIL
    mock_user.insert = AsyncMock()

    with patch('app.services.user_service.User', return_value=mock_user):
        user = await create_user(user_data)

        # Ensure insert was called and the user is created
        mock_user.insert.assert_called_once()
        assert user.email == VALID_EMAIL
        assert user.full_name == "Test User"
        assert user.hashed_password is not None


# Test for getting a user by email
@pytest.mark.asyncio
async def test_get_user_by_email():
    mock_user = MagicMock()
    mock_user.email = VALID_EMAIL

    with patch('app.services.user_service.User.find_one', return_value=mock_user):
        user = await get_user_by_email(VALID_EMAIL)
        assert user.email == VALID_EMAIL


# Test for getting a user by ID
@pytest.mark.asyncio
async def test_get_user_by_id():
    mock_user = MagicMock()
    mock_user.id = VALID_USER_ID

    with patch('app.services.user_service.User.get', return_value=mock_user):
        user = await get_user_by_id(VALID_USER_ID)
        assert user.id == VALID_USER_ID


# Test for activating a user
@pytest.mark.asyncio
async def test_activate_user():
    mock_user = MagicMock()
    mock_user.id = VALID_USER_ID
    mock_user.is_active = False
    mock_user.save = AsyncMock()

    with patch('app.services.user_service.get_user_by_id', return_value=mock_user):
        activated_user = await activate_user(VALID_USER_ID)
        assert activated_user.is_active is True
        mock_user.save.assert_called_once()


# Test for updating user details
@pytest.mark.asyncio
async def test_update_user():
    user_update_data = UserUpdate(full_name="Updated Name", password="newpassword123")
    mock_user = MagicMock()
    mock_user.id = VALID_USER_ID
    mock_user.full_name = "Test User"
    mock_user.hashed_password = "oldhashedpassword"
    mock_user.save = AsyncMock()

    with patch('app.services.user_service.get_user_by_id', return_value=mock_user):
        updated_user = await update_user(VALID_USER_ID, user_update_data)

        assert updated_user.full_name == "Updated Name"
        assert updated_user.hashed_password != "oldhashedpassword"
        mock_user.save.assert_called_once()


# Test for deleting a user
@pytest.mark.asyncio
async def test_delete_user():
    mock_user = MagicMock()
    mock_user.id = VALID_USER_ID
    mock_user.delete = AsyncMock()

    with patch('app.services.user_service.get_user_by_id', return_value=mock_user):
        result = await delete_user(VALID_USER_ID)
        assert result is True
        mock_user.delete.assert_called_once()

