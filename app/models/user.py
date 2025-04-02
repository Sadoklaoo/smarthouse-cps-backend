from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid
import enum


# User Model
class UserRole(enum.Enum):
    ADMIN = "admin"
    RESIDENT = "resident"
    GUEST = "guest"

class User(Base):
    __tablename__ = "users"

    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    devices = relationship("Device", back_populates="user", cascade="all, delete-orphan")
