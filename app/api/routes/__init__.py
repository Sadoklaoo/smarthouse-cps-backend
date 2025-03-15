from fastapi import APIRouter

router = APIRouter()

# Import and include all route modules
from .users import router as users_router
from .devices import router as devices_router
from .events import router as events_router
from .automation import router as automation_router

router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(devices_router, prefix="/devices", tags=["Devices"])
router.include_router(events_router, prefix="/events", tags=["Events"])
router.include_router(automation_router, prefix="/automation", tags=["Automation"])
