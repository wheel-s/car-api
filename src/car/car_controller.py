from fastapi import APIRouter, status, Query
from uuid import UUID
from typing import Annotated

from ..auth.service import currentUser
from ..database.core import DbSession
from . import service
from . import model

from ..resp import Response

router = APIRouter(prefix="/cars", tags=["Cars"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_cars(
    db: DbSession, limit: int = Query(10, ge=1, le=50), page: int = Query(1, ge=1)
):
    cars, count = service.get_all_cars(db, limit, page)
    return {
        "success": "true",
        "code": 200,
        "count": count,
        "data": cars,
    }


@router.get("/spec/{model_name}", status_code=status.HTTP_200_OK)
def get_all_cars_spec(
    db: DbSession,
    model_name: str,
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    car_specs = service.get_spec_by_model(db, model_name, limit, page)
    return car_specs


@router.get(
    "/{car_id}", response_model=model.carResponse, status_code=status.HTTP_200_OK
)
def get_car_by_id(db: DbSession, car_id: UUID):
    return service.get_car_by_id(db, car_id)


@router.get(
    "/search/{model}",
    response_model=list[model.carResponse],
    status_code=status.HTTP_200_OK,
)
def get_cars_by_models(db: DbSession, model: str):
    return service.search_by_model(db, model)


# @router.get("/searchs/{year}",response_model=list[model.carResponse] ,status_code=status.HTTP_200_OK)
# def get_cars_by_models(db:DbSession, model:str):
#     return service.search_by_model(db,model)


@router.post(
    "/createCar", response_model=model.carResponse, status_code=status.HTTP_201_CREATED
)
def create_car(db: DbSession, car_request: model.carCreate, current_user: currentUser):
    return service.create_car(db, car_request, current_user)


@router.put(
    "/{car_id}", response_model=model.carResponse, status_code=status.HTTP_201_CREATED
)
def update_car(
    db: DbSession, car_id: UUID, car_update: model.carUpdate, current_user: currentUser
):
    return service.update_car(db, car_id, car_update, current_user)


@router.delete("/{car_id}", response_model=str, status_code=status.HTTP_200_OK)
def delete_car(db: DbSession, car_id: UUID, current_user: currentUser):
    return service.delete_car(db, car_id, current_user)
