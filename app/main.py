from fastapi import FastAPI
from app.core.database import init_db  # Import the init_db function
import os

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await init_db()  # Initialize the database connection via Beanie
    print("Connected to MongoDB!")

@app.on_event("shutdown")
async def shutdown_db_client():
    if app.mongodb_client:
        app.mongodb_client.close()

@app.get("/")
async def root():
    return {"message": "Smart House Backend running with MongoDB 🚀"}