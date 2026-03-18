from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class favResponse(BaseModel):
    id:UUID
    user_id:UUID
    car_id:UUID


class favCreate(BaseModel):
    car_id:UUID

class favUpdate(BaseModel):
    user_id:Optional[UUID] |None
    car_id:Optional[UUID] |None

