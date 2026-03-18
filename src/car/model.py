from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime









class createBrand(BaseModel):
    name:str
    plant_country:str
    manufacturer:str

class brandResponse(BaseModel):
    id:UUID
    name:str
    plant_country:str
    manufacturer:str


class carCreate(BaseModel):
    brand_id:UUID
    model:str
    year:int
    description:str
    unique_name:str
    favourites:Optional[list[str]] =None


class carUpdate(BaseModel):
    brand_id:UUID
    model:Optional[str] = None
    year:Optional[int] = None
    description:Optional[str] = None
    unique_name:str
    created_at:datetime

class carResponse(BaseModel):
    id:UUID
    user_id:UUID
    brand_id:UUID
    model:str
    year:int
    description:Optional[str] =None
    unique_name:str
    favourites:list[str] =None
    created_at:datetime


class carImageCreate(BaseModel):
    car_id:UUID
    image_url:str
    is_primary:bool = False
    display_order:int = 0

class carImageUpdate(BaseModel):
    image_url:list[str] = None
    car_id:Optional[UUID] = None
    is_primary:bool = False
    display_order:int = 0
    date_added:datetime

class carImageResponse(BaseModel):
    id:UUID
    car_id:UUID
    image_url:list[str]
    is_primary:bool
    display_order:int
    date_added:datetime
