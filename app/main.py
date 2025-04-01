import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import (
    engine,
    async_session,
    Base,
)  # Add the database import here
from sqlalchemy.ext.asyncio import create_async_engine
from app.services.monitor_service import MonitorService
from app.services.reactor_service import ReactorService
from app.services.event_pool import EventPool

DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine for database connection
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Initialize the event pool and reactor service
event_pool = EventPool()
reactor_service = ReactorService(event_pool)

# Initialize monitor service with reactor service
monitor_service = MonitorService(reactor_service)

app = FastAPI(title="Smart House API", version="1.0")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start the house event monitor when the app starts."""
    # Start the monitor service in the background
    monitor_task = asyncio.create_task(monitor_service.monitor_house())
    reactor_task = asyncio.create_task(run_reactor_service())

    # Wait until the app shutdown
    try:
        # This will block until the app is shutdown
        yield
    finally:
        # Cancel the tasks when the app shuts down
        monitor_task.cancel()
        reactor_task.cancel()

        # Cleanup database connections, if needed
        await engine.dispose()
        print("Engine disposed, app shutting down.")


# Use the lifespan context manager for handling events
app.lifespan = lifespan


async def run_reactor_service():
    """Continuously check the EventPool and process events."""
    while True:
        # Check if any events exist in the event pool (this can be adjusted depending on your event handling design)
        events_to_process = event_pool.get_events()  # Access event pool
        for event in events_to_process:
            reactor_service.process_event(event)
        await asyncio.sleep(3)  # Adjust processing interval


# Endpoint for health check or simple test
@app.get("/")
def read_root():
    return {"message": "Hello World"}


# Initialize and create tables when the app starts
@asynccontextmanager
async def startup_database():
    """Create the tables when the app starts."""
    async with engine.begin() as conn:
        # Create all tables in the database if they don't exist
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")
    yield
    # The shutdown process is handled in the `lifespan` context manager.
    # You can add more cleanup code here if needed.


# Add the startup and shutdown functionality to the lifespan handler
app.lifespan = lifespan
