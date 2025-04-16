from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime

class Sensor(Document):
    name: str
    type: str  # e.g., temperature, motion, humidity
    device_id: str  # links to the device it's attached to
    location: Optional[str] = None
    unit: Optional[str] = None  # e.g., °C, %, etc.
    is_active: bool = True
    registered_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "sensors"
        indexes = ["sensor_id", "device_id"]

    class Config:
        json_schema_extra = {
            "example": {
                "sensor_id": "sensor-001",
                "name": "Temp Sensor Living Room",
                "type": "temperature",
                "device_id": "device-123",
                "location": "Living Room",
                "unit": "°C",
                "is_active": True,
            }
        }
