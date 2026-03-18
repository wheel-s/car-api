from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserResponse(BaseModel):
    id:UUID
    email:EmailStr
    username:str

class passwordChange(BaseModel):
    current_password:str
    new_password:str
    new_password_confirm:str

