from beanie import Document
from bson import ObjectId
from pydantic import Field
from typing import Optional
from datetime import datetime

class Sensor(Document):
    name: str
    type: str  # e.g., temperature, motion, humidity
    device_id: ObjectId  # Proper ObjectId reference to Device
    location: Optional[str] = None
    unit: Optional[str] = None  # e.g., °C, %, etc.
    is_active: bool = True
    registered_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "sensors"
        indexes = ["device_id"]

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "Temp Sensor Living Room",
                "type": "temperature",
                "device_id": "6630f4e2f3eab408ae50e02c",
                "location": "Living Room",
                "unit": "°C",
                "is_active": True
            }
        }
