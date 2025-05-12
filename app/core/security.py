from datetime import datetime, timedelta
from typing import Optional
import os
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.services.user_service import get_user_by_email
from app.core.logging_config import logger
from passlib.context import CryptContext

# Secret key - In production, store this in environment variable
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-for-jwt-replace-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

def verify_password(plain_password, hashed_password):
    """Verify that the plain text password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT token with claims."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Dependency to get the current authenticated user from the token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        logger.error("JWT token validation failed")
        raise credentials_exception
    
    user = await get_user_by_email(email=email)
    if user is None:
        logger.error(f"User with email {email} not found")
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure the user is active."""
    if not current_user.is_active:
        logger.warning(f"Inactive user attempt: {current_user.email}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user

def require_roles(required_roles: list):
    """
    Dependency factory: Create a dependency that requires specific roles.
    Usage: Depends(require_roles(["admin"]))
    """
    async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        user_roles = [role.value for role in current_user.roles]
        for role in required_roles:
            if role in user_roles:
                return current_user
        
        logger.warning(f"User {current_user.email} with roles {user_roles} tried to access a resource requiring {required_roles}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required roles: {required_roles}"
        )
    
    return role_checker
