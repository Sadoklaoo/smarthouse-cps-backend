from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.automation import AutomationCreate, AutomationRead
from app.services.automation_service import AutomationService
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=AutomationRead)
async def create_rule(rule: AutomationCreate, db: AsyncSession = Depends(get_db)):
    service = AutomationService(db)
    return await service.create_rule(rule)

@router.get("/", response_model=List[AutomationRead])
async def list_rules(db: AsyncSession = Depends(get_db)):
    service = AutomationService(db)
    return await service.get_all_rules()