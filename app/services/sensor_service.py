import logging
from typing import List, Optional
from fastapi import HTTPException, status
from beanie import PydanticObjectId

from app.models.sensor import Sensor
from app.schemas.sensor import SensorCreate, SensorUpdate
from app.services.device_service import get_device_by_id, get_devices_by_user
from app.services.user_service import get_user_by_id
from beanie.operators import In

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Create a sensor
async def create_sensor(sensor_data: SensorCreate) -> Sensor:
    try:
        logger.info(f"Creating sensor for device: {sensor_data.device_id}")
        
         # ✅ Check if device exists
        device = await get_device_by_id(sensor_data.device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found. Cannot create sensor."
            )
        
        sensor = Sensor(**sensor_data.dict())
        await sensor.insert()
        logger.info(f"Sensor created with ID: {sensor.id}")
        return sensor
    except Exception as e:
        logger.error(f"Error creating sensor: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating sensor: {str(e)}"
        )


# Get a sensor by ID
async def get_sensor_by_id(sensor_id: str) -> Optional[Sensor]:
    try:
        logger.info(f"Fetching sensor by ID: {sensor_id}")
        return await Sensor.get(PydanticObjectId(sensor_id))
    except Exception as e:
        logger.error(f"Error fetching sensor {sensor_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching sensor: {str(e)}"
        )


# Get all sensors
async def get_all_sensors() -> List[Sensor]:
    try:
        logger.info("Fetching all sensors")
        return await Sensor.find_all().to_list()
    except Exception as e:
        logger.error(f"Error fetching all sensors: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching sensors: {str(e)}"
        )


# Get sensors for a specific device
async def get_sensors_by_device_id(device_id: str) -> List[Sensor]:
    try:
        logger.info(f"Fetching sensors for device ID: {device_id}")
        return await Sensor.find(Sensor.device_id == str(device_id)).to_list()
    except Exception as e:
        logger.error(f"Error fetching sensors by device {device_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching sensors: {str(e)}"
        )

# Get sensors for a specific User
async def get_sensors_by_user(user_id: str) -> List[Sensor]:
    try:
        logger.info(f"Fetching sensors for User ID: {user_id}")
        # ✅ Check if user exists
        user = await get_user_by_id(user_id)
        if not user:
            logger.warning(f"User with ID {user_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        # ✅ Step 2: Get devices for the user
        devices = await get_devices_by_user(user_id)
        if not devices:
            logger.info(f"No devices found for user {user_id}")
            return []
        
         # ✅ Step 3: Get sensors for those devices
        device_ids = [str(device.id) for device in devices if device.id is not None]
        if not device_ids:
            logger.warning(f"No valid device IDs for user {user_id}. Skipping sensor query.")
            return []
        
        logger.info(f"Device IDs for user {user_id}: {device_ids}")

        # ✅ Step 4: Fetch sensors for the devices
        sensors = await Sensor.find_many(In(Sensor.device_id, device_ids)).to_list()
        logger.info(f"Found {len(sensors)} sensors for user {user_id}")
        
        return sensors
    except Exception as e:
        logger.error(f"Error fetching sensors by user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching sensors for user: {str(e)}"
        )
    

# Delete a sensor
async def delete_sensor(sensor_id: str) -> bool:
    try:
        logger.info(f"Deleting sensor with ID: {sensor_id}")
        sensor = await get_sensor_by_id(sensor_id)
        if not sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sensor not found"
            )
        await sensor.delete()
        logger.info(f"Sensor {sensor_id} deleted")
        return True
    except Exception as e:
        logger.error(f"Error deleting sensor {sensor_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting sensor: {str(e)}"
        )
