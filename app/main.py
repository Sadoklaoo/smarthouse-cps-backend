import asyncio
from contextlib import asynccontextmanager
import os
from databases import Database
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from app.core.database import create_tables
from app.services import reactor_service
from app.workers.celery_worker import add
from app.services.monitor_service import MonitorService
from sqlalchemy.ext.asyncio import AsyncSession

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="Smart House API", version="1.0")

# Initialize the database connection
database = Database(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start the house event monitor when the app starts."""
    monitor_task = asyncio.create_task(MonitorService.monitor_house())
    reactor_task = asyncio.create_task(run_reactor_service())

    yield
    monitor_task.cancel()
    reactor_task.cancel()


# Use the lifespan context manager for handling events
app.lifespan = lifespan


async def run_reactor_service():
    """Continuously check the EventPool and process events."""
    while True:
        # Check if any events exist in the event pool (this can be adjusted depending on your event handling design)
        events_to_process = reactor_service.event_pool.get_events()
        for event in events_to_process:
            reactor_service.process_event(event)
        await asyncio.sleep(3)  # Adjust processing interval


@app.get("/")
def read_root():
    return {"message": "Hello World"}
