# Initialize routing module
from fastapi import APIRouter
from app.api.routes.user_routes import router as user_router
from app.api.routes.devices_routes import router as device_router
from app.api.routes.sensor_routes import router as sensor_router
from app.api.routes.dashboard_routes import router as dashboard_router
from app.api.routes.monitor_routes import router as monitor_router
from app.api.routes.rule_routes import router as rule_router
from app.api.routes.consequence_routes import router as consequence_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(device_router, prefix="/devices", tags=["Devices"])
api_router.include_router(sensor_router, prefix="/sensors", tags=["Sensors"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(monitor_router, prefix="/monitor", tags=["Monitor"])
api_router.include_router(rule_router, prefix="/rules", tags=["Rules"])
api_router.include_router(consequence_router, prefix="/consequences", tags=["Consequences"])
