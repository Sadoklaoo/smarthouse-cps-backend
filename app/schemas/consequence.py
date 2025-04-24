from pydantic import BaseModel
from datetime import datetime

class ConsequenceRead(BaseModel):
    id: str
    event_id: str
    rule_id: str
    action: str
    device_id: str
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True
