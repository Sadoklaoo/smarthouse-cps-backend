from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.device import DeviceCreate, DeviceResponse, DeviceUpdate
from app.services.device_service import (
    create_device_service,
    get_devices_service,
    get_device_service,
    update_device_status_service,
    delete_device_service,
)
import uuid

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
):
    return create_device_service(device_data, db)

@router.get("/", response_model=list[DeviceResponse])
def get_devices(
    db: Session = Depends(get_db),
):
    return get_devices_service(db)

@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    return get_device_service(device_id, db)

@router.patch("/{device_id}", response_model=DeviceResponse)
def update_device_status(
    device_id: uuid.UUID,
    device_update: DeviceUpdate,
    db: Session = Depends(get_db),
):
    return update_device_status_service(device_id, device_update, db)

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(
    device_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    return delete_device_service(device_id, db)