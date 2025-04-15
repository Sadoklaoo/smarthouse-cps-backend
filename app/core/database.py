# db.py (Initialization for database)

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.models.device import Device
from app.models.sensor import Sensor
from app.models.event import Event
from app.models.automation import Automation
from app.models.action import Action
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# Get MongoDB credentials from environment variables
MONGO_USERNAME = os.getenv("MONGO_USERNAME", "admin")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "admin")
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "smart_house_db")

# Construct MongoDB URI with authentication
MONGODB_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{DATABASE_NAME}?authSource=admin"

client: Optional[AsyncIOMotorClient] = None  # type: ignore

async def init_db():
    global client
    client = AsyncIOMotorClient(MONGODB_URI)  # MongoDB client initialization
    db = client[DATABASE_NAME]

    # Initialize Beanie models
    await init_beanie(
        database=db,
        document_models=[User, Device, Sensor, Event, Automation, Action]
    )

    print("✅ Connected to MongoDB!")