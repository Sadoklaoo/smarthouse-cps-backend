import asyncio
from contextlib import asynccontextmanager
import os
from databases import Database
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from app.core.database import create_tables, get_db, test_database_connection
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
        reactor_service.process_event()
        await asyncio.sleep(3)  # Adjust processing interval


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/test-db")
async def test_db_connection():
    try:
        await create_tables()
        result = await test_database_connection()
        if result == 1:
            return {"message": "Database connection successful!"}
        else:
            raise HTTPException(status_code=500, detail="Unexpected result from DB")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}"
        )


@app.post("/trigger_add/")
async def trigger_add(x: int, y: int):
    task = add.delay(x, y)
    return {"task_id": task.id}
