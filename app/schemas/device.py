from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceCreate(BaseModel):
    device_id: str
    name: str
    type: str
    location: Optional[str] = None

class DeviceRead(BaseModel):
    id: str
    device_id: str
    name: str
    type: str
    location: Optional[str]
    is_active: bool
    registered_at: datetime

    class Config:
        from_attributes = True
