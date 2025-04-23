# Initialize routing module
from fastapi import APIRouter
from app.api.routes.user_routes import router as user_router
from app.api.routes.devices_routes import router as device_router
from app.api.routes.sensor_routes import router as sensor_router
from app.api.routes.dashboard_routes import router as dashboard_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(device_router, prefix="/devices", tags=["Devices"])
api_router.include_router(sensor_router, prefix="/sensors", tags=["Sensors"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
