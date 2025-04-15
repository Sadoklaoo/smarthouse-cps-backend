# app/services/device_service.py
import logging
from typing import Optional, List
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate
from beanie import PydanticObjectId

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # You can change the level to INFO or ERROR depending on your needs

# Creating a new device
async def create_device(device_in: DeviceCreate) -> Device:
    try:
        logger.info(f"Creating device with device_id: {device_in.device_id}")
        device = Device(**device_in.dict())
        await device.insert()
        logger.info(f"Device {device.device_id} created successfully")
        return device
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        raise Exception(f"Error creating device: {e}")


# Getting a device by its device_id
async def get_device_by_id(device_id: str) -> Optional[Device]:
    try:
        logger.info(f"Fetching device with device_id: {device_id}")
        device = await Device.find_one(Device.device_id == device_id)
        if not device:
            logger.warning(f"Device {device_id} not found")
        return device
    except Exception as e:
        logger.error(f"Error fetching device {device_id}: {e}")
        raise Exception(f"Error fetching device {device_id}: {e}")


# Getting all devices for a user
async def get_devices_by_user(user_id: str) -> List[Device]:
    try:
        logger.info(f"Fetching devices for user with user_id: {user_id}")
        devices = await Device.find(Device.user_id == user_id).to_list()
        if not devices:
            logger.warning(f"No devices found for user {user_id}")
        return devices
    except Exception as e:
        logger.error(f"Error fetching devices for user {user_id}: {e}")
        raise Exception(f"Error fetching devices for user {user_id}: {e}")


# Updating a device by its device_id
async def update_device(device_id: str, device_in: DeviceUpdate) -> Optional[Device]:
    try:
        logger.info(f"Updating device with device_id: {device_id}")
        device = await get_device_by_id(device_id)
        if not device:
            logger.warning(f"Device {device_id} not found for update")
            return None
        device_data = device_in.dict(exclude_unset=True)
        for key, value in device_data.items():
            setattr(device, key, value)
        await device.save()
        logger.info(f"Device {device.device_id} updated successfully")
        return device
    except Exception as e:
        logger.error(f"Error updating device {device_id}: {e}")
        raise Exception(f"Error updating device {device_id}: {e}")


# Deleting a device by its device_id
async def delete_device(device_id: str) -> bool:
    try:
        logger.info(f"Deleting device with device_id: {device_id}")
        device = await get_device_by_id(device_id)
        if device:
            await device.delete()
            logger.info(f"Device {device_id} deleted successfully")
            return True
        else:
            logger.warning(f"Device {device_id} not found for deletion")
            return False
    except Exception as e:
        logger.error(f"Error deleting device {device_id}: {e}")
        raise Exception(f"Error deleting device {device_id}: {e}")
