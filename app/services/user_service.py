from typing import Optional
from beanie import PydanticObjectId
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.logging_config import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Create a new user
async def create_user(user_in: UserCreate) -> User:
    try:
        logger.info(f"Creating user with email: {user_in.email}")
        hashed_pw = hash_password(user_in.password)
        user = User(
            email=user_in.email,
            hashed_password=hashed_pw,
            full_name=user_in.full_name
        )
        await user.insert()
        logger.info(f"User created successfully: {user_in.email}")
        return user
    except Exception as e:
        logger.error(f"Error creating user {user_in.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


# Get user by email
async def get_user_by_email(email: str) -> Optional[User]:
    try:
        logger.info(f"Fetching user by email: {email}")
        return await User.find_one(User.email == email)
    except Exception as e:
        logger.error(f"Error fetching user by email {email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user: {str(e)}"
        )


# Get user by ID
async def get_user_by_id(user_id: str) -> Optional[User]:
    try:
        logger.info(f"Fetching user by ID: {user_id}")
        return await User.get(PydanticObjectId(user_id))
    except Exception as e:
        logger.error(f"Error fetching user by ID {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user: {str(e)}"
        )


# Activate a user
async def activate_user(user_id: str) -> Optional[User]:
    try:
        logger.info(f"Activating user with ID: {user_id}")
        user = await get_user_by_id(user_id)
        if not user:
            logger.warning(f"User {user_id} not found for activation")
            return None
        user.is_active = True
        await user.save()
        logger.info(f"User {user_id} activated successfully")
        return user
    except Exception as e:
        logger.error(f"Error activating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error activating user: {str(e)}"
        )


# Update user details
async def update_user(user_id: str, user_in: UserUpdate) -> User:
    try:
        logger.info(f"Updating user with ID: {user_id}")
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        update_data = user_in.dict(exclude_unset=True)
        if "password" in update_data:
            user.hashed_password = hash_password(update_data.pop("password"))
        if "full_name" in update_data:
            user.full_name = update_data["full_name"]

        await user.save()
        logger.info(f"User {user_id} updated successfully")
        return user
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )


# Delete a user
async def delete_user(user_id: str) -> bool:
    try:
        logger.info(f"Deleting user with ID: {user_id}")
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        await user.delete()
        logger.info(f"User {user_id} deleted successfully")
        return True
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )
