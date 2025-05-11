from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.schemas.user import UserCreate, UserRead, UserUpdate, Token, UserLogin
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    update_user,
    delete_user,
    authenticate_user,
)
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user
from app.models.user import User
from app.core.logging_config import logger

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate):
    try:
        logger.info(f"Attempting to register user with email: {user_in.email}")
        existing_user = await get_user_by_email(user_in.email)
        if (existing_user):
            logger.warning(f"User with email {user_in.email} already exists.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists."
            )
        user = await create_user(user_in)
        logger.info(f"User registered successfully with email: {user_in.email}")
        return UserRead(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            roles=user.roles,
            created_at=user.created_at,
            last_login=user.last_login
        )
    except HTTPException as e:
        logger.error(f"Error in registration for email {user_in.email}: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in registration for email {user_in.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registering user: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user(user_id: str):
    try:
        logger.info(f"Fetching user with ID: {user_id}")
        user = await get_user_by_id(user_id)
        if not user:
            logger.warning(f"No user found with ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        return UserRead(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            roles=user.roles,
            created_at=user.created_at,
            last_login=user.last_login
        )
    except HTTPException as e:
        logger.error(f"Error fetching user with ID {user_id}: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching user with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user: {str(e)}"
        )


@router.put("/{user_id}", response_model=UserRead)
async def update_user_route(user_id: str, user_in: UserUpdate):
    try:
        logger.info(f"Updating user with ID: {user_id}")
        user = await update_user(user_id, user_in)
        logger.info(f"User with ID {user_id} updated successfully.")
        return UserRead(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            roles=user.roles,
            created_at=user.created_at,
            last_login=user.last_login
        )
    except HTTPException as e:
        logger.error(f"Error updating user with ID {user_id}: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error updating user with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_route(user_id: str):
    try:
        logger.info(f"Attempting to delete user with ID: {user_id}")
        success = await delete_user(user_id)
        if not success:
            logger.warning(f"User with ID {user_id} not found for deletion.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        logger.info(f"User with ID {user_id} deleted successfully.")
    except HTTPException as e:
        logger.error(f"Error deleting user with ID {user_id}: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error deleting user with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        logger.info(f"Login attempt for user: {form_data.username}")
        user = await authenticate_user(form_data.username, form_data.password)
        if not user:
            logger.warning(f"Failed login attempt for: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token with expiry time
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        logger.info(f"User {form_data.username} logged in successfully")
        return {"access_token": access_token, "token_type": "bearer", "user_id": str(user.id), "roles": [role.value for role in user.roles]}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login for {form_data.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )

@router.post("/token", response_model=Token)
async def login(login_data: UserLogin):
    """Endpoint for login using JSON request instead of form data"""
    try:
        logger.info(f"Login attempt for user: {login_data.email}")
        user = await authenticate_user(login_data.email, login_data.password)
        if not user:
            logger.warning(f"Failed login attempt for: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        
        # Create access token with expiry time
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        logger.info(f"User {login_data.email} logged in successfully")
        return {"access_token": access_token, "token_type": "bearer", "user_id": str(user.id), "roles": [role.value for role in user.roles]}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login for {login_data.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get currently authenticated user's information"""
    return UserRead(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        roles=current_user.roles,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )
