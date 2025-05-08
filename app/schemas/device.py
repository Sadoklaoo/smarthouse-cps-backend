from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class DeviceCreate(BaseModel):
    name: str
    type: str
    location: Optional[str] = None
    user_id: str  # ObjectId of the linked User
    is_active: bool = True
    registered_at: datetime = Field(default_factory=datetime.utcnow)

class DeviceRead(BaseModel):
    id: str
    name: str
    type: str
    location: Optional[str]
    user_id: str
    is_active: bool
    registered_at: datetime
    state: Literal["on", "off"]    

    class Config:
        from_attributes = True

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None
    state: Optional[Literal["on", "off"]] = None
    class Config:
        from_attributes = True
