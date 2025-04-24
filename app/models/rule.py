# models/rule.py
from beanie import Document
from pydantic import Field
from typing import Dict
from datetime import datetime

class Rule(Document):
    name: str
    trigger_type: str  # e.g., "temperature_change"
    condition: Dict[str, float]  # e.g., {"temperature": 28.0}
    operator: str  # ">", "<", "=="
    target_device_id: str
    action: str  # e.g., "turn_on"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "rules"

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "Hot temp triggers AC",
                "trigger_type": "temperature_change",
                "condition": {"temperature": 28.0},
                "operator": ">",
                "target_device_id": "device-123",
                "action": "turn_on"
            }
        }