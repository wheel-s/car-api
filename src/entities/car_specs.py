from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import timezone
from ..database.core import Base


class carSpecs(Base):
    __tablename__ = "car_specs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    car_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cars.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    body_class = Column(String)
    engine_type = Column(String)
    engine_displacement_cylinders = Column(String)
    horsepower = Column(String)
    drivetrain = Column(String)
    torgue = Column(String)
    top_speed = Column(String)
    acceleration = Column(String)
    doors = Column(Integer)
    seats = Column(Integer)
    cargo_volume = Column(String)
    wheel_base = Column(String)
    HWL = Column(String)
    fuel_type = Column(String)
    mpg_tanksize = Column(String)
    price_range = Column(String)
    transmmission = Column(String(50))
    weight = Column(String(50))
    car = relationship("Car", back_populates="specs")
