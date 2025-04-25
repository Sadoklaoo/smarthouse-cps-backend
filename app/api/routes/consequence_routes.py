from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

from app.schemas.consequence import ConsequenceRead
from app.services.consequence_service import (
    get_all_consequences,
    get_consequence_by_id,
    mark_consequence_as_executed
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/", response_model=List[ConsequenceRead], status_code=status.HTTP_200_OK)
async def list_consequences_route():
    try:
        logger.info("Fetching all consequences...")
        consequences = await get_all_consequences()
        return [
            ConsequenceRead(
                id=str(c.id),
                event_id=c.event_id,
                rule_id=c.rule_id,
                action=c.action,
                device_id=c.device_id,
                status=c.status,
                timestamp=c.timestamp
            ) for c in consequences
        ]
    except Exception as e:
        logger.error(f"Error fetching consequences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching consequences: {str(e)}"
        )


@router.get("/{consequence_id}", response_model=ConsequenceRead)
async def get_consequence_route(consequence_id: str):
    try:
        consequence = await get_consequence_by_id(consequence_id)
        return ConsequenceRead(
            id=str(consequence.id),
            event_id=consequence.event_id,
            rule_id=consequence.rule_id,
            action=consequence.action,
            device_id=consequence.device_id,
            status=consequence.status,
            timestamp=consequence.timestamp
        )
    except Exception as e:
        logger.error(f"Error getting consequence {consequence_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting consequence: {str(e)}"
        )


@router.put("/{consequence_id}/execute", response_model=ConsequenceRead)
async def execute_consequence_route(consequence_id: str):
    try:
        updated = await mark_consequence_as_executed(consequence_id)
        return ConsequenceRead(
            id=str(updated.id),
            event_id=updated.event_id,
            rule_id=updated.rule_id,
            action=updated.action,
            device_id=updated.device_id,
            status=updated.status,
            timestamp=updated.timestamp
        )
    except Exception as e:
        logger.error(f"Error executing consequence {consequence_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating consequence: {str(e)}"
        )
