from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    RESIDENT = "resident"
    GUEST = "guest"


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    role: UserRole

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.RESIDENT


class UserUpdateRole(BaseModel):
    role: UserRole