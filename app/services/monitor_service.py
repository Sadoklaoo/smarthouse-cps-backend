from app.core.database import async_session
from app.models.event import Event
from sqlalchemy.future import select
import asyncio
from app.services.event_pool import event_pool


class MonitorService:
    def __init__(self, reactor_service, test_mode=False):
        # Inject reactor_service to avoid circular import
        self.reactor_service = reactor_service
        self.test_mode = test_mode

    @staticmethod
    async def fetch_latest_events():
        """Fetch the latest house events from the database."""
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(Event).order_by(Event.timestamp.desc())
                )
                return result.scalars().all()
        except Exception as e:
            print(f"Error fetching events: {e}")
            return []

    async def monitor_house(self):
        """Continuously monitors house events."""
        loop_count = 0
        while True:
            try:
                events = await MonitorService.fetch_latest_events()
                if events:
                    for event in events:
                        print(
                            f"New Event Detected: {event.event_type} from Device {event.device_id}"
                        )
                        await self.store_event_in_pool(event)
                        await self.reactor_service.handle_event(event)
            except Exception as e:
                print(f"Error during event monitoring: {e}")

            loop_count += 1
            if self.test_mode and loop_count >= 2:  # Run only twice in test mode
                break

            await asyncio.sleep(5)

    @staticmethod
    async def store_event_in_pool(event: Event):
        """Store event in the EventPool."""
        event_data = {
            "id": str(event.id),
            "device_id": str(event.device_id),
            "event_type": event.event_type,
            "timestamp": event.timestamp.isoformat(),
        }
        # Adding event data to the EventPool asynchronously
        await event_pool.add_event(event_data)
