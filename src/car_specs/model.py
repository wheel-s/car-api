from pydantic import BaseModel
from uuid import UUID

# from datetime import datetime
from typing import Optional


class createSpec(BaseModel):
    engine: Optional[str]
    torgue: Optional[str]
    horsepower: Optional[str]
    top_speed: Optional[str]
    acceleration: Optional[str]
    transmission: Optional[str]
    doors: Optional[str]
    seats: Optional[str]
    weight: Optional[str]


class specResponse(BaseModel):
    id: UUID
    engine: str | None = None
    torgue: str | None = None
    horsepower: str | None = None
    top_speed: str | None = None
    acceleration: str | None = None
    transmission: str | None = None
    doors: str | None = None
    seats: str | None = None
    weight: str | None = None
