import datetime
from app.models.consequence import Consequence
from fastapi import HTTPException
from beanie import PydanticObjectId
import logging

logger = logging.getLogger(__name__)

async def get_all_consequences() -> list[Consequence]:
    try:
        return await Consequence.find_all().to_list()
    except Exception as e:
        logger.error(f"Error fetching consequences: {e}")
        raise HTTPException(status_code=500, detail="Error fetching consequences")

async def get_consequence_by_id(consequence_id: str) -> Consequence:
    try:
        consequence = await Consequence.get(PydanticObjectId(consequence_id))
        if not consequence:
            raise HTTPException(status_code=404, detail="Consequence not found")
        return consequence
    except Exception as e:
        logger.error(f"Error fetching consequence {consequence_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching consequence: {str(e)}")

async def mark_consequence_as_executed(consequence_id: str) -> Consequence:
    try:
        consequence = await get_consequence_by_id(consequence_id)
        consequence.status = "executed"
        consequence.executed_at = datetime.datetime.utcnow()
        await consequence.save()
        return consequence
    except Exception as e:
        logger.error(f"Error marking consequence {consequence_id} as executed: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating consequence: {str(e)}")
