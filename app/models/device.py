from beanie import Document, Indexed
from bson import ObjectId
from pydantic import Field
from typing import Optional
from datetime import datetime

class Device(Document):
    name: str
    type: str
    location: Optional[str] = None
    user_id: str  # Proper ObjectId reference to User
    registered_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    class Settings:
        name = "devices"
        indexes = ["user_id"]

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "Smart Light",
                "type": "light",
                "location": "Living Room",
                "user_id": "6630f4e2f3eab408ae50e02b",
                "is_active": True
            }
        }
