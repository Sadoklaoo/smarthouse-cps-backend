from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime

class Device(Document):
    name: str
    type: str  # e.g., light, thermostat
    location: Optional[str]
    status: str = "offline"
    owner_id: Optional[str]  # Reference to User
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "devices"
