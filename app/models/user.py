from beanie import Document,Indexed
from pydantic import EmailStr, Field
from bson import ObjectId
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class User(Document):
    email: EmailStr =  Indexed(unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    roles: List[UserRole] = Field(default=[UserRole.USER])
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Settings:
        name = "users"  # Collection name
    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "hashed_password": "hashed_password_here",
                "full_name": "John Doe",
                "is_active": True,
                "roles": ["user"]
            }
        }