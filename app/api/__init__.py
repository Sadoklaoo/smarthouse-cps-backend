# Initialize API module
from fastapi import FastAPI
from app.api.routes import devices, users, events, auth, automation
from app.core.config import settings


def init_app(app: FastAPI):
    api_prefix = settings.API_V1_STR

    app.include_router(devices.router, prefix=f"{api_prefix}/devices", tags=["Devices"])
    app.include_router(users.router, prefix=f"{api_prefix}/users", tags=["Users"])
    app.include_router(events.router, prefix=f"{api_prefix}/events", tags=["Events"])
    app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["Auth"])
    app.include_router(automation.router, prefix=f"{api_prefix}/automation", tags=["Automation"])
