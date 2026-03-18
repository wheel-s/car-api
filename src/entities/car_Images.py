from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Integer
from  sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..database.core import Base




class CarImages(Base):
    __tablename__ = "car_images"

    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    car_id = Column(UUID(as_uuid=True), ForeignKey('cars.id'), nullable=False)
    image_url = Column(String, nullable= False)
    is_primary = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    date_added = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    car = relationship("Car", back_populates="images")

    def __repr__(self):
        return f"<Image (url = '{self.image_url}') >"