from beanie import Document,Indexed
from pydantic import Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class Automation(Document):
    name: str = Indexed(unique=True)
    description: Optional[str]
    trigger: Dict[str, Any]  # e.g., {"sensor_type": "temperature", "value_gt": 25}
    conditions: Optional[List[Dict[str, Any]]]
    is_enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "automations"
        indexes = ["name"]
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Cool Down Room",
                "description": "Turn on fan if temperature > 25",
                "trigger": {"sensor_type": "temperature", "value_gt": 25},
                "conditions": [{"room": "Living Room"}],
                "is_enabled": True
            }
        }
