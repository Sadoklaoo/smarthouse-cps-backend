from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    RESIDENT = "resident"
    GUEST = "guest"


class UserResponse(BaseModel):
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)  # Use ConfigDict instead of class-based Config


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.RESIDENT


class UserUpdateRole(BaseModel):
    role: UserRole