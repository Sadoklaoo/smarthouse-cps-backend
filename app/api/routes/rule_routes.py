import logging
from typing import List
from fastapi import APIRouter, HTTPException, status

from app.schemas.rule import RuleCreate, RuleRead
from app.services.rule_service import (
    create_rule,
    get_all_rules,
    delete_rule_by_id,
)
from app.models.rule import Rule

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/", response_model=RuleRead, status_code=status.HTTP_201_CREATED)
async def create_rule_route(rule_in: RuleCreate):
    try:
        logger.info(f"Creating rule: {rule_in.name}")
        rule = await create_rule(rule_in)
        return RuleRead(
            id=str(rule.id),
            name=rule.name,
            trigger_type=rule.trigger_type,
            condition=rule.condition,
            operator=rule.operator,
            target_device_id=rule.target_device_id,
            action=rule.action,
            created_at=rule.created_at
        )
    except Exception as e:
        logger.error(f"Error creating rule: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating rule: {str(e)}"
        )


@router.get("/", response_model=List[RuleRead])
async def list_rules_route():
    try:
        logger.info("Fetching all rules...")
        rules = await get_all_rules()
        return [
            RuleRead(
                id=str(rule.id),
                name=rule.name,
                trigger_type=rule.trigger_type,
                condition=rule.condition,
                operator=rule.operator,
                target_device_id=rule.target_device_id,
                action=rule.action,
                created_at=rule.created_at
            ) for rule in rules
        ]
    except Exception as e:
        logger.error(f"Error fetching rules: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching rules: {str(e)}"
        )


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule_route(rule_id: str):
    try:
        logger.info(f"Deleting rule {rule_id}")
        success = await delete_rule_by_id(rule_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rule not found"
            )
        logger.info(f"Rule {rule_id} deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting rule {rule_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting rule: {str(e)}"
        )
