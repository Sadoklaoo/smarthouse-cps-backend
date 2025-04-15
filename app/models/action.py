from beanie import Document
from pydantic import Field
from typing import Literal, Optional, Dict
from datetime import datetime

class Action(Document):
    target_device_id: str
    action_type: Literal["turn_on", "turn_off", "set_temp", "notify"]
    parameters: Optional[Dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "actions"
