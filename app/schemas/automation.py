from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class AutomationCreate(BaseModel):
    name: str
    description: Optional[str] = None
    trigger: Dict[str, Any]
    conditions: Optional[List[Dict[str, Any]]] = None
    is_enabled: bool = True

class AutomationRead(BaseModel):
    id: str
    name: str
    description: Optional[str]
    trigger: Dict[str, Any]
    conditions: Optional[List[Dict[str, Any]]]
    is_enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True
