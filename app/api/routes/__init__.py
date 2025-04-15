# Initialize routing module
from fastapi import APIRouter
from app.api.routes.user_routes import router as user_router
from app.api.routes.devices_routes import router as device_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(device_router, prefix="/devices", tags=["devices"])
