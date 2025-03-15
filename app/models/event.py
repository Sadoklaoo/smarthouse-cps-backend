

from sqlalchemy import Column, String, UUID, TIMESTAMP, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid

from app.models.device import Device

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=False)
    event_type = Column(String(255), nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())

    device = relationship("Device", back_populates="events")

Device.events = relationship("Event", back_populates="device", cascade="all, delete-orphan")
