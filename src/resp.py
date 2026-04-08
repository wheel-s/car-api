from pydantic import BaseModel
from typing import List, Any

from .car_specs.model import specResponse


class Response(BaseModel):
    success: bool
    data: Any
    code: int

    model_config = {"from_attributes": True}
