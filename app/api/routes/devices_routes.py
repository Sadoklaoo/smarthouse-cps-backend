# app/api/routes/device_routes.py
import logging
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from app.services.device_service import create_device, get_device_by_id, get_devices_by_user, update_device, delete_device

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set log level as needed

router = APIRouter()

# Create a new device
@router.post("/", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
async def create_device_route(device_in: DeviceCreate):
    try:
        logger.info(f"Attempting to create device with device_id: {device_in.device_id}")
        device = await create_device(device_in)
        return DeviceRead(
            id=str(device.id),
            device_id=device.device_id,
            name=device.name,
            type=device.type,
            location=device.location,
            is_active=device.is_active,
            registered_at=device.registered_at
        )
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Update an existing device
@router.put("/{device_id}", response_model=DeviceRead)
async def update_device_route(device_id: str, device_in: DeviceUpdate):
    try:
        logger.info(f"Attempting to update device with device_id: {device_id}")
        device = await update_device(device_id, device_in)
        if not device:
            logger.warning(f"Device {device_id} not found for update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
        return DeviceRead(
            id=str(device.id),
            device_id=device.device_id,
            name=device.name,
            type=device.type,
            location=device.location,
            is_active=device.is_active,
            registered_at=device.registered_at
        )
    except Exception as e:
        logger.error(f"Error updating device {device_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Delete a device
@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device_route(device_id: str):
    try:
        logger.info(f"Attempting to delete device with device_id: {device_id}")
        success = await delete_device(device_id)
        if not success:
            logger.warning(f"Device {device_id} not found for deletion")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
    except Exception as e:
        logger.error(f"Error deleting device {device_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Get all devices for a specific user
@router.get("/user/{user_id}", response_model=List[DeviceRead])
async def get_devices_for_user(user_id: str):
    try:
        logger.info(f"Fetching devices for user_id: {user_id}")
        devices = await get_devices_by_user(user_id)

        if not devices:
            logger.warning(f"No devices found for user_id: {user_id}")
            return []  # Still returns 200 but empty list

        device_list = [
            DeviceRead(
                id=str(device.id),
                device_id=device.device_id,
                name=device.name,
                type=device.type,
                location=device.location,
                is_active=device.is_active,
                registered_at=device.registered_at
            )
            for device in devices
        ]

        logger.info(f"Fetched {len(device_list)} devices for user_id: {user_id}")
        return device_list

    except Exception as e:
        logger.exception(f"Error fetching devices for user_id: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while fetching user's devices"
        )

# Get device by id
@router.get("/{device_id}", response_model=DeviceRead)
async def get_device(device_id: str):
    try:
        logger.info(f"Fetching device with device_id: {device_id}")
        device = await get_device_by_id(device_id)
        if not device:
            logger.warning(f"Device {device_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
        return DeviceRead(
            id=str(device.id),
            device_id=device.device_id,
            name=device.name,
            type=device.type,
            location=device.location,
            is_active=device.is_active,
            registered_at=device.registered_at
        )
    except Exception as e:
        logger.error(f"Error fetching device {device_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
