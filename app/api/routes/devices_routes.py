import logging
from typing import List, Literal
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from app.services.device_service import (
    create_device,
    get_device_by_id,
    get_devices_by_user,
    set_device_state,
    update_device,
    delete_device,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
async def create_device_route(device_in: DeviceCreate):
    try:
        logger.info("Creating new device...")
        device = await create_device(device_in)
        return DeviceRead(
            id=str(device.id),
            name=device.name,
            type=device.type,
            location=device.location,
            user_id=str(device.user_id),
            is_active=device.is_active,
            registered_at=device.registered_at
        )
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating device: {str(e)}"
        )


@router.get("/{device_id}", response_model=DeviceRead)
async def get_device(device_id: str):
    try:
        logger.info(f"Fetching device with ID: {device_id}")
        device = await get_device_by_id(device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
        return DeviceRead(
            id=str(device.id),
            name=device.name,
            type=device.type,
            location=device.location,
            user_id=str(device.user_id),
            is_active=device.is_active,
            registered_at=device.registered_at
        )
    except Exception as e:
        logger.error(f"Error fetching device {device_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching device: {str(e)}"
        )


@router.get("/user/{user_id}", response_model=List[DeviceRead])
async def get_devices_for_user(user_id: str):
    try:
        logger.info(f"Fetching devices for user_id: {user_id}")
        devices = await get_devices_by_user(user_id)
        if not devices:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No devices found for this user"
            )
        return [
            DeviceRead(
                id=str(device.id),
                name=device.name,
                type=device.type,
                location=device.location,
                user_id=str(device.user_id),
                is_active=device.is_active,
                registered_at=device.registered_at
            )
            for device in devices
        ]
    except Exception as e:
        logger.error(f"Error fetching devices for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error fetching user's devices: {str(e)}"
        )
@router.get("/", response_model=List[DeviceRead])
async def get_devices():
    try:
        logger.info(f"Fetching all devices ")
        devices = await get_devices()
        if not devices:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No devices found "
            )
        return [
            DeviceRead(
                id=str(device.id),
                name=device.name,
                type=device.type,
                location=device.location,
                user_id=str(device.user_id),
                is_active=device.is_active,
                registered_at=device.registered_at
            )
            for device in devices
        ]
    except Exception as e:
        logger.error(f"Error fetching devices  {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error fetching devices: {str(e)}"
        )

@router.put("/{device_id}", response_model=DeviceRead)
async def update_device_route(device_id: str, device_in: DeviceUpdate):
    try:
        logger.info(f"Updating device {device_id}")
        device = await update_device(device_id, device_in)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
        return DeviceRead(
            id=str(device.id),
            name=device.name,
            type=device.type,
            location=device.location,
            user_id=str(device.user_id),
            is_active=device.is_active,
            registered_at=device.registered_at
        )
    except Exception as e:
        logger.error(f"Error updating device {device_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating device: {str(e)}"
        )


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device_route(device_id: str):
    try:
        logger.info(f"Deleting device {device_id}")
        success = await delete_device(device_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
        logger.info(f"Device {device_id} deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting device {device_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting device: {str(e)}"
        )


class StateUpdate(BaseModel):
    state: Literal["on", "off"]

@router.post("/{device_id}/state", response_model=DeviceRead, status_code=status.HTTP_200_OK)
async def update_device_state_route(device_id: str, body: StateUpdate):
    updated = await set_device_state(device_id, body.state)
    return DeviceRead(
        id=str(updated.id),
        name=updated.name,
        type=updated.type,
        location=updated.location,
        user_id=updated.user_id,
        is_active=updated.is_active,
        state=updated.state,
        registered_at=updated.registered_at
    )