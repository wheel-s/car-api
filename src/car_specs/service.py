from fastapi import HTTPException

from sqlalchemy.orm import Session
from ..entities.car_specs import carSpecs

# from ..entities.cars import Brand, Car
from . import model
from ..auth.models import TokenData
from uuid import UUID
import logging

logger = logging.getLogger("cars")


def get_specs(db: Session):
    specs = db.query(carSpecs).limit(9).all()
    logger.info(f"Retrieved all car spec")
    return specs


def get_spec_by_id(db: Session, spec_id: UUID) -> model.specResponse:
    spec = db.query(carSpecs).filter(carSpecs.id == spec_id).first()
    if not spec:
        logger.info(f"retreived spec {spec_id}")
        raise HTTPException(status_code=404, detail=f"spec not found {spec_id}")
    logger.info(f"retrieved spec {spec_id}")
    return spec


def create_spec(
    db: Session, spec_create: model.createSpec, current_user: TokenData
) -> model.specResponse:
    try:
        spec = carSpecs(**spec_create.model_dump())
        db.add(spec)
        db.commit()
        db.refresh()
        logger.info(f"Created new spec with user: {current_user.get_uuid()}")
        return spec
    except Exception as e:
        logger.info(f"")
        raise


def update_spec(
    db: Session, spec_id: UUID, spec_update: model.createSpec, current_user: TokenData
) -> model.specResponse:
    spec_data = spec_update.model_dump(exclude_unset=True)
    db.query(carSpecs).filter(carSpecs.id == spec_id).update(spec_data)
    db.commit()
    logger.info(f"")
    return get_spec_by_id(db, spec_id)


def delete_spec(db: Session, spec_id: UUID, current_user: TokenData) -> str:
    spec = get_spec_by_id(db, spec_id)
    db.delete(spec)
    db.commit()
    logger.info(f"spec {spec_id} deleted by user {current_user.get_uuid()}")
    return f"Successfully deleted car_spec"
