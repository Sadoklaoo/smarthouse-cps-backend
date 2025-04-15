from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.automation import Automation
from app.schemas.automation import AutomationCreate

class AutomationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_rule(self, automation_data: AutomationCreate):
        new_rule = Automation(**automation_data.dict())
        self.db.add(new_rule)
        await self.db.commit()
        await self.db.refresh(new_rule)
        return new_rule

    async def get_all_rules(self):
        result = await self.db.execute(select(Automation))
        return result.scalars().all()

    async def evaluate_rules(self, event: dict):
        """Simulate evaluation like: {'device_id': ..., 'type': 'motion', 'value': 'detected'}"""
        rules = await self.get_all_rules()
        for rule in rules:
            if rule.condition in str(event):
                print(f"✅ Rule triggered: {rule.condition} ➔ Action: {rule.action}")