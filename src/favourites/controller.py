from fastapi import APIRouter, status
from typing import List, Annotated

from uuid import UUID
from .. auth.service import currentUser
from ..database.core import DbSession
from . import model
from . import service






router  = APIRouter(
    prefix='/favourites',
    tags=['Favourites']
)




@router.get("/", status_code=status.HTTP_200_OK)
def get_favourites(db:DbSession, current_user:currentUser):
    return service.get_favourites(db, current_user.get_uuid())


@router.post("/", status_code=status.HTTP_200_OK)
def get_favourites(db:DbSession, fav_create:model.favCreate ,current_user:currentUser):
    return service.create_favourites(db, fav_create ,current_user.get_uuid())



@router.delete("/{car_id}", status_code=status.HTTP_200_OK)
def get_favourites(db:DbSession, car_id:UUID ,current_user:currentUser):
    return service.unfavourite_car(db, car_id,current_user.get_uuid())

