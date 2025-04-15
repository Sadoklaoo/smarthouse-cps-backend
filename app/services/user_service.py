# app/services/user_service.py
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate,UserUpdate
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.logging_config import logger  # Import the logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def create_user(user_in: UserCreate) -> User:
    try:
        logger.info(f"Creating user with email: {user_in.email}")  # Log user creation attempt
        hashed_pw = hash_password(user_in.password)
        user = User(
            email=user_in.email,
            hashed_password=hashed_pw,
            full_name=user_in.full_name
        )
        await user.insert()
        logger.info(f"User created successfully with email: {user_in.email}")  # Log success
        return user
    except Exception as e:
        logger.error(f"Error creating user with email {user_in.email}: {str(e)}")  # Log error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


async def get_user_by_email(email: str) -> Optional[User]:
    try:
        logger.info(f"Fetching user by email: {email}")  # Log fetch attempt
        user = await User.find_one(User.email == email)
        if user:
            logger.info(f"User found with email: {email}")  # Log success
        else:
            logger.warning(f"No user found with email: {email}")  # Log warning
        return user
    except Exception as e:
        logger.error(f"Error fetching user by email {email}: {str(e)}")  # Log error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user by email: {str(e)}"
        )


async def get_user_by_id(user_id: str) -> Optional[User]:
    try:
        logger.info(f"Fetching user by ID: {user_id}")  # Log fetch attempt
        user = await User.get(user_id)
        if user:
            logger.info(f"User found with ID: {user_id}")  # Log success
        else:
            logger.warning(f"No user found with ID: {user_id}")  # Log warning
        return user
    except Exception as e:
        logger.error(f"Error fetching user by ID {user_id}: {str(e)}")  # Log error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user by ID: {str(e)}"
        )


async def activate_user(user_id: str) -> Optional[User]:
    try:
        logger.info(f"Activating user with ID: {user_id}")  # Log activation attempt
        user = await get_user_by_id(user_id)
        if user:
            user.is_active = True
            await user.save()
            logger.info(f"User with ID: {user_id} activated successfully.")  # Log success
        else:
            logger.warning(f"User with ID: {user_id} not found for activation.")  # Log warning
        return user
    except Exception as e:
        logger.error(f"Error activating user with ID {user_id}: {str(e)}")  # Log error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error activating user: {str(e)}"
        )

async def update_user(user_id: str, user_in: UserUpdate) -> User:
    try:
        # Fetch the user by ID
        user = await User.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update the user fields
        user.email = user_in.email or user.email
        user.full_name = user_in.full_name or user.full_name
        user.is_active = user_in.is_active if user_in.is_active is not None else user.is_active

        # Save updated user data
        await user.save()
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )

async def delete_user(user_id: str) -> bool:
    try:
        user = await User.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Delete the user from the database
        await user.delete()
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )