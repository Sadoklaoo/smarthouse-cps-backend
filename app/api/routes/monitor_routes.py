# routes/monitor_routes.py
import datetime
from fastapi import APIRouter
from app.queues.event_producer import enqueue_event
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

@router.post("/trigger")
async def trigger_event():
    event = {
        "type": "temperature_change",
        "sensor_id": "abc123",
        "temperature": 26,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    await enqueue_event(event)
    return {"message": "Event queued", "event": event}