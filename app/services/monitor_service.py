from app.core.database import async_session
from app.models.event import Event
from sqlalchemy.future import select
import asyncio
from app.services.event_pool import event_pool


# MonitorService class to fetch latest events
class MonitorService:
    async def fetch_latest_events():
        """Fetch the latest house events from the database."""
        async with async_session() as session:
            result = await session.execute(
                select(Event).order_by(Event.timestamp.desc())
            )
            return result.scalars().all()

    async def monitor_house():
        """Continuously monitors house events."""
        while True:
            events = await MonitorService.fetch_latest_events()
            for event in events:
                print(
                    f"New Event Detected: {event.event_type} from Device {event.device_id}"
                )
                # Future: Store in EventPool or trigger ReactorService
            await asyncio.sleep(5)  # Adjust interval as needed

    def store_event_in_pool(event: Event):
        event_data = {
            "id": str(event.id),
            "device_id": str(event.device_id),
            "event_type": event.event_type,
            "timestamp": event.timestamp.isoformat(),
        }
        event_pool.add_event(event_data)
