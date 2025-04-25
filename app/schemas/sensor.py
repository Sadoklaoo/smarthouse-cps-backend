from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorCreate(BaseModel):
    name: str
    type: str
    device_id: str  # ObjectId of the linked Device
    location: Optional[str] = None
    unit: Optional[str] = None

class SensorRead(BaseModel):
    id: str
    name: str
    type: str
    device_id: str
    location: Optional[str]
    unit: Optional[str]
    is_active: bool
    registered_at: datetime

    class Config:
        from_attributes = True

class SensorUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    device_id: Optional[str] = None  # ObjectId of the linked Device
    location: Optional[str] = None
    unit: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        # You can add any custom configurations here if needed
        from_attributes = True