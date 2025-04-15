from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AutomationCreate(BaseModel):
    condition: str
    action: str
    device_id: UUID

class AutomationRead(BaseModel):
    id: UUID
    condition: str
    action: str
    device_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True