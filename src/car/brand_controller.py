from fastapi import APIRouter
from fastapi import APIRouter, status, Query
from uuid import UUID
from typing import Annotated

# from ..auth.service import currentUser
from ..database.core import DbSession
from . import service
from . import model

brand_router = APIRouter(prefix="/brands", tags=["Brand"])


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
