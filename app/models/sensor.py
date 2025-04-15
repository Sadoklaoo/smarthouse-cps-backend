from beanie import Document
from pydantic import Field
from typing import Literal, Optional
from datetime import datetime

class Sensor(Document):
    name: str
    device_id: str  # Parent device
    type: Literal["temperature", "motion", "humidity", "camera"]
    value: Optional[float] = None
    unit: Optional[str]
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "sensors"
