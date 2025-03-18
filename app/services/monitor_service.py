from app.core.database import async_session
from app.models.event import Event
from sqlalchemy.future import select


# MonitorService class to fetch latest events
class MonitorService:
    async def fetch_latest_events():
        async with async_session() as session:
            result = await session.execute(select(Event).order_by(Event.timestamp.desc()))
            return result.scalars().all()