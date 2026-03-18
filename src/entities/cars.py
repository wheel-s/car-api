from sqlalchemy import Column,Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid 
from ..database.core import Base





class Brand(Base):
    __tablename__ = "brands"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)
    plant_country = Column(String)
    manufacturer = Column(String)
    cars = relationship("Car", back_populates="brand")





class Car(Base):
    __tablename__ = "cars"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),ForeignKey('users.id'), nullable=False )
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id', ondelete='RESTRICT'), nullable=False, index=True)
    model =  Column(String(50), nullable=False, index=True)
    year = Column(Integer,nullable=False,index=True)
    description =Column(String)
    unique_name=Column(String, nullable =False, unique=True, index=True)
    brand = relationship("Brand", back_populates="cars", uselist=False, )
    specs = relationship("carSpecs", back_populates='car', cascade="all, delete-orphan")
    images = relationship('CarImages', back_populates='car')
    fans = relationship('User', secondary="favourites", back_populates='favourites')
    created_at=Column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
  
    def __repr__(self):
        return f"<car (make='{self.model}') >"