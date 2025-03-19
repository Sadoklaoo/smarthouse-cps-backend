from app.workers.celery_worker import celery
from app.services.monitor_service import MonitorService
from app.services.reactor_service import reactor  # type: ignore
import asyncio

# This task will be executed every 5 minutes
# It will fetch the latest events from the monitor service
# and process them using the reactor service


@celery.task
def process_events():
    events = asyncio.run(MonitorService.fetch_latest_events())
    for event in events:
        reactor.process_event(event)
