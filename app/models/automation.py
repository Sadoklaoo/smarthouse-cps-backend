from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid

class Automation(Base):
    __tablename__ = "automation_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    condition = Column(String(255), nullable=False)  # e.g. "motion=detected"
    action = Column(String(255), nullable=False)     # e.g. "turn_on_light"
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    device = relationship("Device", back_populates="automation")
