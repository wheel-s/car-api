from sqlalchemy import Column, String, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
import enum
import uuid
from ..database.core import Base


class Role(str, enum.Enum):
    admin = "ADMIN"
    user = "USER"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.user)
    favourites = relationship("Car", secondary="favourites", back_populates="fans")
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f"<user(name = '{self.id}' User succesfully created)>"
