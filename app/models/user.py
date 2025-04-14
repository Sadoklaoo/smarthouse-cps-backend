from sqlalchemy import Column, String, UUID, TIMESTAMP, ForeignKey, Enum, Boolean
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
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # Store hashed passwords
    role = Column(Enum(UserRole), default=UserRole.RESIDENT, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())