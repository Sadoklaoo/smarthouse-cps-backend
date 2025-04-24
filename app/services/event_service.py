# services/event_service.py
from app.models.event import Event
from app.schemas.event import EventCreate
from fastapi import HTTPException
import logging

from app.services.reactor_service import process_event

logger = logging.getLogger(__name__)

async def log_event(event_in: EventCreate) -> Event:
    try:
        event = Event(**event_in.dict())
        await event.insert()
        logger.info(f"Logged event for device {event.device_id} of type {event.event_type}")
        
         # 🧠 Trigger the reactor
        await process_event(event)
        
        return event
    except Exception as e:
        logger.error(f"Error logging event: {e}")
        raise HTTPException(status_code=500, detail=f"Error logging event: {str(e)}")
