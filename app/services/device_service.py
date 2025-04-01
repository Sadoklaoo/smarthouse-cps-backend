import logging
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.device import Device
from app.models.user import User
from app.schemas.device import DeviceCreate, DeviceUpdate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_device_service(device_data: DeviceCreate, db: Session, current_user: User):
    """Creates a new device and associates it with the current user."""
    logger.info(f"Creating device for user {current_user.id}")
    device = Device(
        device_name=device_data.device_name,
        device_type=device_data.device_type,
        status=device_data.status,
        user_id=current_user.id,
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    logger.info(f"Device {device.id} created successfully")
    return device

def get_devices_service(db: Session, current_user: User):
    """Retrieves all devices associated with the current user."""
    logger.info(f"Fetching devices for user {current_user.id}")
    return db.query(Device).filter(Device.user_id == current_user.id).all()

def get_device_service(device_id: uuid.UUID, db: Session, current_user: User):
    """Retrieves a specific device owned by the current user."""
    logger.info(f"Fetching device {device_id} for user {current_user.id}")
    device = db.query(Device).filter(Device.id == device_id, Device.user_id == current_user.id).first()
    if not device:
        logger.warning(f"Device {device_id} not found for user {current_user.id}")
        raise HTTPException(status_code=404, detail="Device not found")
    return device

def update_device_status_service(device_id: uuid.UUID, device_update: DeviceUpdate, db: Session, current_user: User):
    """Updates the status of a device owned by the current user."""
    logger.info(f"Updating status of device {device_id} for user {current_user.id}")
    device = db.query(Device).filter(Device.id == device_id, Device.user_id == current_user.id).first()
    if not device:
        logger.warning(f"Device {device_id} not found for update by user {current_user.id}")
        raise HTTPException(status_code=404, detail="Device not found")
    
    if device_update.status is not None:
        device.status = device_update.status
    
    db.commit()
    db.refresh(device)
    logger.info(f"Device {device_id} status updated successfully")
    return device

def delete_device_service(device_id: uuid.UUID, db: Session, current_user: User):
    """Deletes a device owned by the current user."""
    logger.info(f"Deleting device {device_id} for user {current_user.id}")
    device = db.query(Device).filter(Device.id == device_id, Device.user_id == current_user.id).first()
    if not device:
        logger.warning(f"Device {device_id} not found for deletion by user {current_user.id}")
        raise HTTPException(status_code=404, detail="Device not found")
    
    db.delete(device)
    db.commit()
    logger.info(f"Device {device_id} deleted successfully")
    return None