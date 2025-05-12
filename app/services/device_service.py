import logging
from typing import Literal, Optional, List

from bson import ObjectId
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate
from beanie import PydanticObjectId
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Create a new device
async def create_device(device_in: DeviceCreate) -> Device:
    try:
        logger.info("Creating new device...")
        device = Device(**device_in.dict())
        await device.insert()
        logger.info(f"Device created successfully with ID: {device.id}")
        return device
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating device: {str(e)}"
        )


# Get a device by MongoDB ObjectId
async def get_device_by_id(device_id: str) -> Optional[Device]:
    try:
        logger.info(f"Fetching device by ID: {device_id}")
        device = await Device.get(PydanticObjectId(device_id))
        if not device:
            logger.warning(f"Device with ID {device_id} not found")
        return device
    except Exception as e:
        logger.error(f"Error fetching device {device_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching device: {str(e)}"
        )


# Get all devices for a given user (by ObjectId)
async def get_devices_by_user(user_id: str) -> List[Device]:
    try:
        logger.info(f"Fetching devices for user: {user_id}")
        devices = await Device.find(Device.user_id == user_id).to_list()
        logger.info(f"Found {len(devices)} devices for user ID: {user_id}")
        return devices
    except Exception as e:
        logger.error(f"Error fetching devices for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching devices: {str(e)}"
        )


async def get_all_devices() -> List[Device]:
    try:
        # Fetch every document in the devices collection
        return await Device.find_all().to_list()
    except Exception as e:
        logger.error(f"Error fetching all devices: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching devices: {str(e)}"
        )


# Update a device by ID
async def update_device(device_id: str, device_in: DeviceUpdate) -> Optional[Device]:
    try:
        logger.info(f"Updating device with ID: {device_id}")
        device = await get_device_by_id(device_id)
        if not device:
            logger.warning(f"Device {device_id} not found for update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )

        device_data = device_in.dict(exclude_unset=True)
        for key, value in device_data.items():
            setattr(device, key, value)

        await device.save()
        logger.info(f"Device {device_id} updated successfully")
        return device
    except Exception as e:
        logger.error(f"Error updating device {device_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating device: {str(e)}"
        )


# Delete a device by ID
async def delete_device(device_id: str) -> bool:
    try:
        logger.info(f"Deleting device with ID: {device_id}")
        device = await get_device_by_id(device_id)
        if not device:
            logger.warning(f"Device {device_id} not found for deletion")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
        await device.delete()
        logger.info(f"Device {device_id} deleted successfully")
        return True
    except Exception as e:
        logger.error(f"Error deleting device {device_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting device: {str(e)}"
        )

# Set device state (on/off)
async def set_device_state(device_id: str, state: Literal["on", "off"]) -> Device:
    # Validate state
    if state not in ("on", "off"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid state '{state}', must be 'on' or 'off'"
        )

    # Fetch device
    device = await get_device_by_id(device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )

    # Update and save
    device.state = state
    device.registered_at = device.registered_at   # preserve existing timestamp
    await device.save()
    return device