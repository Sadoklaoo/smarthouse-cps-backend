# app/schemas/device.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceCreate(BaseModel):
    device_id: str
    name: str
    type: str
    location: Optional[str] = None
    user_id: str  # Associate with a user
    is_active: bool = True
    registered_at: datetime = Field(default_factory=datetime.utcnow)

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

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None
