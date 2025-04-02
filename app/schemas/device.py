import uuid
from pydantic import BaseModel
from sqlalchemy import Enum


class DeviceTypeEnum(str, Enum):
    LIGHT = "light"
    THERMOSTAT = "thermostat"
    SENSOR = "sensor"

class DeviceCreate(BaseModel):
    device_name: str
    device_type: DeviceTypeEnum
    status: bool = False
    
    class Config:
        arbitrary_types_allowed = True

class DeviceResponse(BaseModel):
    id: uuid.UUID
    device_name: str
    device_type: DeviceTypeEnum
    status: bool
    user_id: uuid.UUID

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class DeviceUpdate(BaseModel):
    status: bool | None = None
