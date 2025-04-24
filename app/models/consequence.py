# models/consequence.py
from beanie import Document
from pydantic import Field
from datetime import datetime

class Consequence(Document):
    event_id: str
    rule_id: str
    action: str
    device_id: str
    status: str = "pending"  # or "executed"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "consequences"


    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "event_id": "event123",
                "rule_id": "rule456",
                "action": "turn_on",
                "device_id": "device-123",
                "status": "pending"
            }
        }