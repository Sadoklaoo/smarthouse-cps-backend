from app.models.rule import Rule
from app.schemas.rule import RuleCreate
from fastapi import HTTPException
import logging
from typing import List
import operator
logger = logging.getLogger(__name__)


OPERATORS = {
    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq,
    ">=": operator.ge,
    "<=": operator.le
}
async def get_matching_rules(event: dict) -> List[Rule]:
    all_rules = await Rule.find_all().to_list()
    matched_rules = []

    for rule in all_rules:
        if rule.trigger_type != event.get("type"):
            continue
        
        # Example: rule.condition = {"temperature": 28.0}
        for key, value in rule.condition.items():
            if key not in event:
                continue
            event_value = event[key]
            op = OPERATORS.get(rule.operator)
            if op and op(event_value, value):
                matched_rules.append(rule)

    return matched_rules

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
