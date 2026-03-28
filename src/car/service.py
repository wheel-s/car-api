from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from ..auth.models import TokenData
from fastapi import HTTPException
from ..entities.cars import Car, Brand
from ..entities.car_specs import carSpecs
from ..entities.car_Images import CarImages
from . import model
import logging

logger = logging.getLogger("cars")


def get_all_brands(db: Session, limit, page) -> list[model.brandResponse]:
    offset = limit * (page - 1)
    brand = db.query(Brand).offset(offset).limit(limit).all()
    logger.info(f"Retrieved all {brand} car data")
    return brand


def get_all_cars_by_brands(
    db: Session, brand_name: str, limit, page
) -> list[model.carResponse]:
    offset = limit * (page - 1)
    brand = db.query(Brand).filter(Brand.name.ilike(f"%{brand_name}%")).first()
    if brand:
        cars = (
            db.query(Car)
            .filter(Car.brand_id == brand.id)
            .offset(offset)
            .limit(limit)
            .all()
        )
        logger.info(f"Retrieved all  car data")
        return cars
    return []


def get_brand_by_id(db: Session, brand_id: UUID) -> model.brandResponse:
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    logger.info(f"Retrieved all {brand} car data")
    return brand


def get_all_cars(db: Session, limit, page) -> list[model.carResponse]:
    offset = limit * (page - 1)
    cars = db.query(Car).offset(offset).limit(limit).offset(offset).limit(limit).all()
    logger.info(f"Retrieved all  car data")
    return cars


def get_car_and_brands_by_year(db: Session, year: int, brand_name: str, limit, page):
    offset = limit * (page - 1)
    brand = db.query(Brand).filter(Brand.name.ilike(f"%{brand_name}%")).first()
    cars = (
        db.query(Car)
        .filter(Car.brand_id == brand.id)
        .filter(Car.year == year)
        .offset(offset)
        .limit(limit)
        .all()
    )
    logger.info(f"Retrieved all  car data")
    return cars


def get_spec_by_model(db: Session, model_name: str, limit, page):
    print(model_name)
    car = db.query(Car).filter(Car.unique_name.ilike(f"%{model_name}%")).first()
    spec = db.query(carSpecs).filter(carSpecs.car_id == car.id).first()
    logger.info(f"Retrieved all  car data")
    return spec


def get_car_by_id(db: Session, car_id: UUID) -> model.carResponse:
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        logger.info(f"Failed to retrieve car with id: {car_id}")
        raise HTTPException(status_code=404, detail="car data not found")
    logger.info(f"rettrieved car with id: {car_id}")
    return car


def search_by_model(db: Session, model: str):
    cars = db.query(Car).filter(Car.model.ilike(f"%{model}%")).all()
    if not cars:
        logger.info(f"Failed to retrieve car with id: {model}")
        raise HTTPException(status_code=404, detail="car data not found")
    logger.info(f"rettrieved car with id: {model}")
    return cars


def create_brand(
    db: Session, brand_request: model.createBrand, current_user: TokenData
):
    try:
        brand_car = Car(
            id=uuid4(), user_id=current_user.get_uuid(), brand=brand_request.brand
        )
        db.add(brand_car)
        db.commit()
        db.refresh(brand_car)
        logger.info(f"Created new todo for user : {current_user.get_uuid()}")
        return brand_car
    except Exception as e:
        logger.error(
            f"Failed to create car {brand_request.brand}", extra={"Error": str(e)}
        )
        raise HTTPException(status_code=500, detail=str(e))


def create_car(
    db: Session, car_request: model.carCreate, current_user: TokenData
) -> model.carResponse:
    try:
        new_car = Car(
            id=uuid4(),
            user_id=current_user.get_uuid(),
            make=car_request.make,
            model=car_request.model,
            year=car_request.year,
            description=car_request.description,
            unique_name=f"{car_request.make}_{car_request.model}_{car_request.year}",
        )
        db.add(new_car)
        db.commit()
        db.refresh(new_car)
        logger.info(f"Created new todo for user : {current_user.get_uuid()}")
        return new_car
    except Exception as e:
        logger.error(
            f"Failed to create car {car_request.model}", extra={"Error": str(e)}
        )
        raise HTTPException(status_code=500, detail=str(e))


def update_car(
    db: Session, car_id: UUID, car_update: model.carUpdate, current_user: TokenData
):
    car_data = car_update.model_dump(exclude_unset=True)
    db.query(Car).filter(Car.id == car_id).update(car_data)
    db.commit()
    logger.info(f"Sucessfully uppdated todo fro user {current_user.get_uuid()}")
    return get_car_by_id(db, car_id)


def delete_car(db: Session, car_id: UUID, current_user: TokenData) -> str:
    car = get_car_by_id(db, car_id)
    db.delete(car)
    db.commit()
    logger.info(f"Car {car_id} deleted by user {current_user.get_uuid()}")
    return f"Sucessfully deleted car"


def get_images(db: Session) -> list[model.carImageResponse]:
    images = db.query(CarImages).all()
    logger.info(f"retrieved all car images")
    return images


def get_image_by_id(db: Session, image_id=UUID) -> model.carImageResponse:
    image = db.query(CarImages).filter(CarImages.id == image_id).first()
    if not image:
        logger.info(f"Failed to retreive image {image_id}")
        raise HTTPException(status_code=404, detail=f"car image {image_id} not found")
    logger.info(f"Retreived car image {image_id}")
    return image


def create_Image(
    db: Session, image: model.carImageCreate, current_user: TokenData
) -> model.carImageResponse:
    try:
        Image = CarImages(**image.model_dump())
        db.add(Image)
        db.commit()
        db.refresh(Image)
        logger.info(f"Createsd new car image {image.car_id}")
        return Image
    except Exception as e:
        logger.info(f"Failed to create car image by user: {current_user.get_uuid()}")
        raise


def update_image(
    db: Session,
    image_id: UUID,
    image_update: model.carImageUpdate,
    current_user: TokenData,
) -> model.carImageResponse:
    image_data = image_update.model_dump(exclude_unset=True)
    db.query(CarImages).filter(CarImages.id == image_id).update(image_data)
    db.commit()
    logger.info(f"")
    return get_image_by_id(db, image_id)


def append_image(
    db: Session,
    image_id: UUID,
    image_update: model.carImageUpdate,
    current_user: TokenData,
) -> model.carImageResponse:
    image_data = image_update.model_dump(exclude_unset=True)
    db_image = get_image_by_id(db, image_id)

    if "image_url" in image_data and image_data["image_url"]:
        current = db_image.image_url + image_data["image_url"]
        db_image.image_url = current

    if "car_id" in image_data and image_data["car_id"]:
        db_image = image_data["car_id"]

    db.commit()
    db.refresh(db_image)
    logger.info(f"done")
    return db_image


def delete_image(db: Session, image_id: UUID, current_user: TokenData) -> str:
    image = get_image_by_id(db, image_id)
    db.delete(image)
    db.commit()
    logger.info(f"Car {image_id} deleted by user {current_user.get_uuid()}")
    return f"Successfully deleted car image"
