from beanie import Document
from pydantic import Field
from typing import List
from datetime import datetime

class Automation(Document):
    name: str
    condition: str  # e.g., "temp > 30"
    actions: List[str]  # list of Action IDs
    is_enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "automations"
