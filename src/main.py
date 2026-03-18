from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from .database.core import engine, Base
from .entities.users import User
from .entities.cars import Brand, Car
from .entities.car_Images import CarImages
from .entities.car_specs import carSpecs
from .entities.favourites import favourites
from typing import Annotated


from .api import register_routes

app = FastAPI()

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

register_routes(app)
from. logging import setup_logging, get_logger


#setup_logging()

logger = get_logger("app")

@app.get("/")
def get_all(request:Request, name:Annotated[str | None, Query(max_length=20)]):
    logger.info(f"halpdsc", extra={"Ip":request.client.host, "url":request.url.path})
    print(name)
    return {"status": "Success"}
    

