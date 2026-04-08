from fastapi import FastAPI
from src.users.controller import router as users_router
from src.auth.controller import router as auth_router

# from src.make.controller import router as todo_router
from src.car.car_controller import router as car_router
from src.car.image_controller import image_router
from src.car_specs.controller import router as specs_router
from src.car.brand_controller import brand_router
from src.favourites.controller import router as fav_router


def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(users_router)
    # app.include_router(todo_router)
    app.include_router(brand_router)
    app.include_router(car_router)
    app.include_router(image_router)
    app.include_router(specs_router)
    app.include_router(fav_router)
