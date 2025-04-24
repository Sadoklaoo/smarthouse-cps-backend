from fastapi import FastAPI
from app.core.database import init_db  # Import the init_db function
from app.api.routes import api_router  # Import the API router
import os
import asyncio
from app.queues.reactor_worker import consume_events

app = FastAPI()

app.include_router(api_router, prefix="/api", tags=["API"])

@app.on_event("startup")
async def startup_db_client():
    await init_db()  # Initialize the database connection via Beanie
    print("Connected to MongoDB!")
    asyncio.create_task(consume_events())
    print("Event Consumer Started!")

@app.on_event("shutdown")
async def shutdown_db_client():
    if app.mongodb_client:
        app.mongodb_client.close()

@app.get("/")
async def root():
    return {"message": "Smart House Backend running with MongoDB 🚀"}