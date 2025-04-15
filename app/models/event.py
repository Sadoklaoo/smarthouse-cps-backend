from beanie import Document
from pydantic import Field
from typing import Optional, Dict
from datetime import datetime

class Event(Document):
    source: str  # Sensor or device ID
    type: str  # e.g., "motion_detected", "temp_threshold_exceeded"
    payload: Optional[Dict] = None
    triggered_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "events"
