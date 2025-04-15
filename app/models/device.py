from beanie import Document, Indexed
from pydantic import Field
from typing import Optional
from datetime import datetime

class Device(Document):
    device_id: str = Indexed(unique=True)
    name: str
    type: str
    location: Optional[str] = None
    user_id: str  # Link to User
    registered_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    class Settings:
        name = "devices"
        indexes = ["device_id", "user_id"]

    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "device-123",
                "name": "Smart Light",
                "type": "light",
                "location": "Living Room",
                "user_id": "6630f4e2f3eab408ae50e02b",
                "is_active": True
            }
        }
