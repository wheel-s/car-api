from fastapi import APIRouter, status, Query
from uuid import UUID
from typing import Annotated

from ..auth.service import currentUser
from ..database.core import DbSession
from . import service
from . import model

image_router = APIRouter(prefix="/images", tags=["Images"])


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
