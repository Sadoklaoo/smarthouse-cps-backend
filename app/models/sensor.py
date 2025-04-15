from beanie import Document,Indexed
from pydantic import Field
from typing import Optional
from datetime import datetime

class Sensor(Document):
    sensor_id: str = Indexed(unique=True)
    device_id: str
    type: str
    unit: Optional[str] = None
    last_value: Optional[float] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "sensors"
        indexes = ["sensor_id"]
    class Config:
        json_schema_extra = {
            "example": {
                "sensor_id": "sensor-xyz",
                "device_id": "device-123",
                "type": "temperature",
                "unit": "Celsius",
                "last_value": 23.5
            }
        }
