from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID  # Correct import for UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid
import enum

from app.models.device import Device


class Automation(Base):
    __tablename__ = "automation_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    condition = Column(String(255), nullable=False)
    action = Column(String(255), nullable=False)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    device = relationship("Device", back_populates="automation")


Device.automation = relationship(
    "Automation", back_populates="device", cascade="all, delete-orphan"
)
