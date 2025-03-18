from celery import Celery
from app.core.config import settings
from celery.schedules import crontab

# Create a Celery instance
celery = Celery(
    "smart_house",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Set the Celery configuration
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

# Define the Celery beat schedule
# This schedule will run the process_events task every 10 seconds
celery.conf.beat_schedule = {
    "process-events-every-10-seconds": {
        "task": "app.workers.tasks.process_events",
        "schedule": 10.0,  # Runs every 10 seconds
    },
}

# This is where you can define periodic tasks if necessary
@celery.task
def add(x, y):
    return x + y