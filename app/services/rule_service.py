from app.models.rule import Rule
from app.schemas.rule import RuleCreate
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def create_rule(rule_in: RuleCreate) -> Rule:
    try:
        rule = Rule(**rule_in.dict())
        await rule.insert()
        logger.info(f"Created rule: {rule.name}")
        return rule
    except Exception as e:
        logger.error(f"Error creating rule: {e}")
        raise HTTPException(status_code=500, detail="Error creating rule")


async def get_all_rules() -> list[Rule]:
    try:
        return await Rule.find_all().to_list()
    except Exception as e:
        logger.error(f"Error fetching rules: {e}")
        raise HTTPException(status_code=500, detail="Error fetching rules")


async def delete_rule_by_id(rule_id: str) -> bool:
    try:
        rule = await Rule.get(rule_id)
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        await rule.delete()
        return True
    except Exception as e:
        logger.error(f"Error deleting rule: {e}")
        raise HTTPException(status_code=500, detail="Error deleting rule")
