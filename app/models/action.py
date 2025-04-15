from beanie import Document,Indexed
from pydantic import Field
from typing import Dict, Any
from datetime import datetime

class Action(Document):
    automation_id: str = Indexed()
    action_type: str  # e.g., "turn_on"
    parameters: Dict[str, Any]  # e.g., {"device_id": "fan-1"}
    executed_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "actions"
        indexes = ["automation_id"]
    class Config:
        json_schema_extra = {
            "example": {
                "automation_id": "automation-abc",
                "action_type": "turn_on",
                "parameters": {"device_id": "fan-1"}
            }
        }
