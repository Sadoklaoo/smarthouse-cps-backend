from app.core.database import async_session
from app.models.event import Event
from sqlalchemy.future import select
import asyncio
from app.services.event_pool import event_pool
from app.services.reactor_service import reactor_service  # Assuming this is your ReactorService

class MonitorService:
    @staticmethod
    async def fetch_latest_events():
        """Fetch the latest house events from the database."""
        async with async_session() as session:
            result = await session.execute(
                select(Event).order_by(Event.timestamp.desc())
            )
            return result.scalars().all()

    @staticmethod
    async def monitor_house():
        """Continuously monitors house events."""
        while True:
            events = await MonitorService.fetch_latest_events()
            if events:
                for event in events:
                    print(
                        f"New Event Detected: {event.event_type} from Device {event.device_id}"
                    )
                    # Store event in EventPool
                    MonitorService.store_event_in_pool(event)
                    # Trigger the ReactorService to process the event
                    reactor_service.process_events()  # Assuming process_events handles the reactor logic
            await asyncio.sleep(5)  # Adjust interval as needed

    @staticmethod
    def store_event_in_pool(event: Event):
        """Store event in the EventPool."""
        event_data = {
            "id": str(event.id),
            "device_id": str(event.device_id),
            "event_type": event.event_type,
            "timestamp": event.timestamp.isoformat(),
        }
        # Adding event data to the EventPool
        event_pool.add_event(event_data)
