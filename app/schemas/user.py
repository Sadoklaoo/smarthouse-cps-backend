from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.models.user import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    roles: Optional[List[UserRole]] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    roles: List[str]

class TokenData(BaseModel):
    email: Optional[str] = None
    roles: Optional[List[str]] = None

class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    roles: List[UserRole]
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    roles: Optional[List[UserRole]] = None

    class Config:
        from_attributes = True
