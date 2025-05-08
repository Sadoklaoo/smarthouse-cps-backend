from fastapi import FastAPI
from app.core.database import init_db  # Import the init_db function
from app.api.routes import api_router  # Import the API router
import os
import asyncio
from app.queues.reactor_worker import consume_events
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration: Allow requests from localhost:3000 (React app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


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