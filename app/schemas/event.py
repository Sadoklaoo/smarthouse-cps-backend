from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class EventCreate(BaseModel):
    device_id: str
    event_type: str
    data: Dict[str, float]

class EventRead(BaseModel):
    id: str
    device_id: str
    event_type: str
    data: Dict[str, float]
    timestamp: datetime

    class Config:
        orm_mode = True
