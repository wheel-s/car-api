from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from ..database.core import Base
from enum import Enum

favourites = Table(
    "favourites",
    Base.metadata,
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    ),
    Column(
        "car_id",
        UUID(as_uuid=True),
        ForeignKey("cars.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    ),
)


class UserRole(str, Enum):
    guest = ("guest",)
    user = ("user",)
    admin = "admin"
