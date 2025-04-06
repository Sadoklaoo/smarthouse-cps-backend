from sqlalchemy import BINARY, Column, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid
import sqlalchemy
from app.models.device import Device


class Automation(Base):
    __tablename__ = "automations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    device_id = Column(UUID(as_uuid=True), ForeignKey('devices.id')) 

    name = Column(String(255), nullable=False)
    condition = Column(String(255), nullable=False)  # Define the condition for automation
    action = Column(String(255), nullable=False)  # Define the action to be taken
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    device = relationship("Device", back_populates="automations")

Device.automations = relationship(
    "Automation", back_populates="device", cascade="all, delete-orphan"
)
