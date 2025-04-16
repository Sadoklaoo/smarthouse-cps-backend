from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.sensor import SensorCreate, SensorRead
from app.services.sensor_service import (
    create_sensor,
    get_sensor_by_id,
    get_all_sensors,
    get_sensors_by_device_id,
    delete_sensor
)
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=SensorRead)
async def register_sensor(sensor: SensorCreate):
    try:
        logger.info(f"Registering sensor: {sensor.sensor_id}")
        sensor_doc = await create_sensor(sensor)
        return SensorRead(**sensor_doc.dict(), id=str(sensor_doc.id))
    except Exception as e:
        logger.error(f"Error creating sensor: {e}")
        raise HTTPException(status_code=500, detail="Sensor creation failed.")

@router.get("/", response_model=List[SensorRead])
async def get_all():
    try:
        sensors = await get_all_sensors()
        return [SensorRead(**s.dict(), id=str(s.id)) for s in sensors]
    except Exception as e:
        logger.error(f"Error fetching all sensors: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sensors.")

@router.get("/device/{device_id}", response_model=List[SensorRead])
async def get_by_device(device_id: str):
    try:
        sensors = await get_sensors_by_device_id(device_id)
        return [SensorRead(**s.dict(), id=str(s.id)) for s in sensors]
    except Exception as e:
        logger.error(f"Error fetching sensors by device_id {device_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sensors for device.")

@router.get("/{sensor_id}", response_model=SensorRead)
async def get_sensor(sensor_id: str):
    try:
        sensor = await get_sensor_by_id(sensor_id)
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor not found")
        return SensorRead(**sensor.dict(), id=str(sensor.id))
    except Exception as e:
        logger.error(f"Error fetching sensor {sensor_id}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching sensor.")

@router.delete("/{sensor_id}")
async def delete(sensor_id: str):
    try:
        if await delete_sensor(sensor_id):
            return {"message": "Sensor deleted successfully"}
        raise HTTPException(status_code=404, detail="Sensor not found")
    except Exception as e:
        logger.error(f"Error deleting sensor {sensor_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting sensor.")
