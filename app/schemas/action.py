from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class ActionCreate(BaseModel):
    automation_id: str
    action_type: str
    parameters: Dict[str, Any]

class ActionRead(BaseModel):
    id: str
    automation_id: str
    action_type: str
    parameters: Dict[str, Any]
    executed_at: datetime

    class Config:
        orm_mode = True
