# routes/monitor_routes.py
from fastapi import APIRouter
from app.schemas.event import EventCreate, EventRead
from app.services.event_service import log_event
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=EventRead)
async def create_event(event: EventCreate):
    logger.info(f"Monitoring event: {event.event_type}")
    saved_event = await log_event(event)
    return EventRead(
        id=str(saved_event.id),
        device_id=saved_event.device_id,
        event_type=saved_event.event_type,
        data=saved_event.data,
        timestamp=saved_event.timestamp
    )
