from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

from app.schemas.sensor import SensorCreate, SensorRead
from app.services.sensor_service import (
    create_sensor,
    get_sensor_by_id,
    get_all_sensors,
    get_sensors_by_device_id,
    delete_sensor
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=SensorRead, status_code=status.HTTP_201_CREATED)
async def register_sensor(sensor: SensorCreate):
    try:
        sensor_doc = await create_sensor(sensor)
        return SensorRead(
            id=str(sensor_doc.id),
            name=sensor_doc.name,
            type=sensor_doc.type,
            device_id=str(sensor_doc.device_id),
            location=sensor_doc.location,
            unit=sensor_doc.unit,
            is_active=sensor_doc.is_active,
            registered_at=sensor_doc.registered_at
        )
    except Exception as e:
        logger.error(f"Error creating sensor: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sensor creation failed"
        )


@router.get("/", response_model=List[SensorRead])
async def get_all():
    try:
        sensors = await get_all_sensors()
        return [
            SensorRead(
                id=str(s.id),
                name=s.name,
                type=s.type,
                device_id=str(s.device_id),
                location=s.location,
                unit=s.unit,
                is_active=s.is_active,
                registered_at=s.registered_at
            ) for s in sensors
        ]
    except Exception as e:
        logger.error(f"Error fetching all sensors: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch sensors"
        )


@router.get("/device/{device_id}", response_model=List[SensorRead])
async def get_by_device(device_id: str):
    try:
        sensors = await get_sensors_by_device_id(device_id)
        return [
            SensorRead(
                id=str(s.id),
                name=s.name,
                type=s.type,
                device_id=str(s.device_id),
                location=s.location,
                unit=s.unit,
                is_active=s.is_active,
                registered_at=s.registered_at
            ) for s in sensors
        ]
    except Exception as e:
        logger.error(f"Error fetching sensors for device {device_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch sensors for device"
        )


@router.get("/{sensor_id}", response_model=SensorRead)
async def get_sensor(sensor_id: str):
    try:
        sensor = await get_sensor_by_id(sensor_id)
        if not sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sensor not found"
            )
        return SensorRead(
            id=str(sensor.id),
            name=sensor.name,
            type=sensor.type,
            device_id=str(sensor.device_id),
            location=sensor.location,
            unit=sensor.unit,
            is_active=sensor.is_active,
            registered_at=sensor.registered_at
        )
    except Exception as e:
        logger.error(f"Error fetching sensor {sensor_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching sensor"
        )


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(sensor_id: str):
    try:
        success = await delete_sensor(sensor_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sensor not found"
            )
        logger.info(f"Sensor with ID {sensor_id} deleted successfully.")
    except Exception as e:
        logger.error(f"Error deleting sensor {sensor_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting sensor"
        )
