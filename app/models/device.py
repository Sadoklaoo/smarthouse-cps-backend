from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID  # Correct import for UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid
import enum

from app.models.user import User


class DeviceType(enum.Enum):
    LIGHT = "light"
    THERMOSTAT = "thermostat"
    SENSOR = "sensor"


class Device(Base):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_name = Column(String(255), nullable=False)
    device_type = Column(Enum(DeviceType), nullable=False)
    status = Column(Boolean, default=False, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="devices")


User.devices = relationship(
    "Device", back_populates="user", cascade="all, delete-orphan"
)
