from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_device_service(device_data: DeviceCreate, db: Session):
    """Creates a new device."""
    logger.info("[DeviceService] Creating new device: %s", device_data.device_name)
    new_device = Device(**device_data.dict())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    logger.info("[DeviceService] Device created successfully with ID: %s", new_device.id)
    return new_device

def get_devices_service(db: Session):
    """Retrieves all devices."""
    logger.info("[DeviceService] Fetching all devices")
    return db.query(Device).all()

def get_device_service(device_id: uuid.UUID, db: Session):
    """Retrieves a device by ID."""
    logger.info("[DeviceService] Fetching device with ID: %s", device_id)
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        logger.warning("[DeviceService] Device not found: %s", device_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return device

def update_device_status_service(device_id: uuid.UUID, device_update: DeviceUpdate, db: Session):
    """Updates a device status."""
    logger.info("[DeviceService] Updating device status for ID: %s", device_id)
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        logger.warning("[DeviceService] Device not found for update: %s", device_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    
    for key, value in device_update.dict(exclude_unset=True).items():
        setattr(device, key, value)
    
    db.commit()
    db.refresh(device)
    logger.info("[DeviceService] Device updated successfully: %s", device_id)
    return device

def delete_device_service(device_id: uuid.UUID, db: Session):
    """Deletes a device by ID."""
    logger.info("[DeviceService] Deleting device with ID: %s", device_id)
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        logger.warning("[DeviceService] Device not found for deletion: %s", device_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    
    db.delete(device)
    db.commit()
    logger.info("[DeviceService] Device deleted successfully: %s", device_id)
    return {"detail": f"Device with ID {device_id} deleted successfully"}
