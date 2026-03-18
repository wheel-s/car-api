from uuid import UUID, uuid4
from sqlalchemy.orm import Session 
from ..auth.models import TokenData
from fastapi import HTTPException

from ..entities.favourites import favourites
from sqlalchemy import select, insert, delete
from ..entities.cars import Car
from  ..auth.service import currentUser
from . import model

import logging


logger = logging.getLogger("favourites")


def get_favourites(db:Session,user_id:TokenData):
    stmt = select(favourites.c.car_id).where(favourites.c.user_id == user_id)
    result = db.execute(stmt)
    car = result.scalars().all()
    return car

def get_cars_for_user_fav(db:Session, user_id):
    stmt = (
        select(Car)
        .join(favourites, Car.id==favourites.c.car_id)
        .where(favourites.c.user_id == user_id)
    )
    result = db.execute(stmt)
    car = result.scalars().all()
    return car


def create_favourites(db:Session, fav_create:model.favCreate, user_id:TokenData):
    stmt = insert(favourites).values(
        user_id = user_id,
        car_id = fav_create.car_id
    )
    db.execute(stmt)
    db.commit()
    return "successfully added car to favourites"



def unfavourite_car(db:Session,car_id ,user_id):
    stmt = delete(favourites).where(
        favourites.c.user_id == user_id,
        favourites.c.car_id == car_id
    )
    db.execute(stmt)
    db.commit()
    return "sucessfully deleted favourites"