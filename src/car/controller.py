from fastapi import APIRouter, status, Query
from uuid import UUID
from typing import Annotated

from ..auth.service import currentUser
from ..database.core import DbSession
from . import service
from . import model

router = APIRouter(prefix="/cars", tags=["Cars"])

brand_router = APIRouter(prefix="/brands", tags=["Brand"])

image_router = APIRouter(prefix="/images", tags=["Images"])


@brand_router.get(
    "/cars", response_model=list[model.carResponse], status_code=status.HTTP_200_OK
)
def get_all_brands_by_name(
    db: DbSession,
    name: Annotated[str | None, Query(max_length=20)],
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    print(name)
    return service.get_all_cars_by_brands(db, name, limit, page)


@brand_router.get(
    "/", response_model=list[model.brandResponse], status_code=status.HTTP_200_OK
)
def get_all_brands(
    db: DbSession, limit: int = Query(10, ge=1, le=20), page: int = Query(1, ge=1)
):
    return service.get_all_brands(db, limit, page)


@brand_router.get("/{brand_id}", status_code=status.HTTP_200_OK)
def get_brand_by_id(
    db: DbSession,
    brand_id: UUID,
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    return service.get_brand_by_id(db, brand_id)


@brand_router.get("/{brand_name}/year/{year}", status_code=status.HTTP_200_OK)
def get_all_brand_by_year_brand(
    db: DbSession,
    year: int,
    brand_name: str,
    limit: int = Query(9, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    return service.get_car_and_brands_by_year(db, year, brand_name, limit, page)


@router.get("/model/{model_name}", status_code=status.HTTP_200_OK)
def get_all_cars_spec(
    db: DbSession,
    model_name: str,
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    return service.get_spec_by_model(db, model_name, limit, page)


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_cars(
    db: DbSession, limit: int = Query(10, ge=1, le=50), page: int = Query(1, ge=1)
):
    return service.get_all_cars(db, limit, page)


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


@image_router.get(
    "/", response_model=list[model.carImageResponse], status_code=status.HTTP_200_OK
)
def get_car_images(db: DbSession):
    return service.get_images(db)


@image_router.get(
    "/{image_id}", response_model=model.carImageResponse, status_code=status.HTTP_200_OK
)
def get_image_by_id(db: DbSession, image_id: UUID):
    return service.get_image_by_id(db, image_id)


@image_router.post(
    "/", response_model=model.carImageResponse, status_code=status.HTTP_201_CREATED
)
def create_car_image(
    db: DbSession, image: model.carImageCreate, current_user: currentUser
):
    return service.create_Image(db, image, current_user)


@image_router.put(
    "/{image_id}",
    response_model=model.carImageResponse,
    status_code=status.HTTP_201_CREATED,
)
def update_car_image(
    db: DbSession,
    image_id: UUID,
    image_update: model.carImageUpdate,
    current_user: currentUser,
):
    return service.append_image(db, image_id, image_update, current_user)


@image_router.delete("/{image_id}", response_model=str, status_code=status.HTTP_200_OK)
def delete_image(db: DbSession, image_id: UUID, current_user: currentUser):
    return service.delete_image(db, image_id, current_user)
