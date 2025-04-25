from beanie import Document,Indexed
from pydantic import Field
from typing import Dict
from datetime import datetime

class Event(Document):
    device_id: str
    event_type: str
    data: Dict[str, float]  # e.g., {"temperature": 23.5}
    timestamp: datetime = Field(default_factory=datetime.utcnow)


    class Settings:
        name = "events"
        indexes = ["timestamp"]
    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "device_id": "device-123",
                "event_type": "temperature_change",
                "data": {"temperature": 23.5}
            }
        }
