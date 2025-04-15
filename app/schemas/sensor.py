from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorCreate(BaseModel):
    sensor_id: str
    device_id: str
    type: str
    unit: Optional[str] = None

class SensorRead(BaseModel):
    id: str
    sensor_id: str
    device_id: str
    type: str
    unit: Optional[str]
    last_value: Optional[float]
    last_updated: datetime

    class Config:
        from_attributes = True
