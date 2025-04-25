from fastapi import APIRouter, HTTPException
from app.services.user_service import get_user_by_id
from app.services.device_service import get_devices_by_user
from app.services.sensor_service import get_sensors_by_device_id
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/{user_id}")
async def get_user_dashboard(user_id: str):
    try:
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        devices = await get_devices_by_user(user_id)
        result = []

        for device in devices:
            sensors = await get_sensors_by_device_id(str(device.id))  # Cast if sensor.device_id is str
            sensor_data = [
                {
                    "id": str(s.id),
                    "name": s.name,
                    "type": s.type,
                    "unit": s.unit,
                    "is_active": s.is_active
                }
                for s in sensors
            ]

            result.append({
                "id": str(device.id),
                "name": device.name,
                "type": device.type,
                "location": device.location,
                "is_active": device.is_active,
                "sensors": sensor_data
            })

        return {
            "user_id": user_id,
            "devices": result
        }

    except Exception as e:
        logger.error(f"Error building dashboard for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")
