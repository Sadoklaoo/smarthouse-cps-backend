from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorCreate(BaseModel):
    sensor_id: str
    name: str
    type: str
    device_id: str
    location: Optional[str] = None
    unit: Optional[str] = None

class SensorRead(BaseModel):
    id: str
    sensor_id: str
    name: str
    type: str
    device_id: str
    location: Optional[str]
    unit: Optional[str]
    is_active: bool
    registered_at: datetime

    class Config:
        from_attributes = True
