from typing import Optional
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
    executed_at: Optional[datetime] = None 

    class Config:
        from_attributes = True
