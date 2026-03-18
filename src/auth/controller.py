from typing import Annotated
from fastapi import APIRouter, Depends, Request
from starlette import status
from . import models
from . import service
from fastapi.security import OAuth2PasswordRequestForm
from ..database.core import DbSession
from ..rate_limiting import limiter


router = APIRouter(
    prefix = '/auth',
    tags=['auth']
)



@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/hour")
async def register_user(request:Request, db:DbSession, register_user_request: models.RegisterUser):
    service.register_user(db, register_user_request)
    return {"message":"Successfully registered user"}

@router.post("/token", response_model=models.Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db:DbSession):
    print(f"{form_data}")
    return service.login_for_access_token(form_data, db)
    