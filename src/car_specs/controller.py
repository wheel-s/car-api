from fastapi import APIRouter, status
from uuid import UUID

from ..database.core import DbSession
from src.auth.service import currentUser
from . import model
from . import service

router = APIRouter(prefix="/specs", tags=["Specs"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_specs(db: DbSession):
    return service.get_specs(db)


@router.get("/{spec_id}", status_code=status.HTTP_200_OK)
def get_spec_by_id(db: DbSession, spec_id: UUID):
    return service.get_spec_by_id(db, spec_id)


@router.post("/", response_model=model.createSpec, status_code=status.HTTP_201_CREATED)
def create_spec(db: DbSession, spec: model.createSpec, current_user: currentUser):
    return


@router.put("/{spec_id}", status_code=status.HTTP_201_CREATED)
def update_spec(
    db: DbSession,
    spec_id: UUID,
    spec_update: model.createSpec,
    current_user: currentUser,
):
    return


@router.delete("/{spec_id}", response_model=str, status_code=status.HTTP_200_OK)
def delete_spec(db: DbSession, spec_id: UUID, current_user: currentUser):
    return
