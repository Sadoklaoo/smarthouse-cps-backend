from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class RuleCreate(BaseModel):
    name: str
    trigger_type: str  # e.g., "temperature_change"
    condition: Dict[str, float]  # e.g., {"temperature": 28.0}
    operator: str  # e.g., ">", "<", "=="
    target_device_id: str
    action: str  # e.g., "turn_on"

class RuleRead(BaseModel):
    id: str
    name: str
    trigger_type: str
    condition: Dict[str, float]
    operator: str
    target_device_id: str
    action: str
    created_at: datetime

    class Config:
        from_attributes = True
