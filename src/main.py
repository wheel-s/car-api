from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from starlette.responses import Response
from urllib.parse import urlencode
from starlette.exceptions import HTTPException as StarleteHTTPException
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .database.core import engine, Base
from .entities.users import User
from .entities.cars import Brand, Car
from .entities.car_Images import CarImages
from .entities.car_specs import carSpecs
from .entities.favourites import favourites
from typing import Annotated
import time
import os
import httpx
from dotenv import load_dotenv

load_dotenv()


from .api import register_routes

PRODUCTION = False
app = FastAPI(
    docs_url=None if PRODUCTION else "/docs",
    redoc_url=None if PRODUCTION else "/redoc",
    openapi_url=None if PRODUCTION else "/openapi.json",
)

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


register_routes(app)
from .logging import setup_logging, get_logger

# setup_logging()

logger = get_logger("app")

replica = os.getenv("APP_NAME")


@app.get("/", response_class=HTMLResponse)
def get_all(request: Request):
    logger.info(f"halpdsc", extra={"Ip": request.client.host, "url": request.url.path})
    # name: Annotated[str | None, Query(max_length=20)]
    # print(name)
    return """
            <h2> Welcome to FastAPI Google OAuth2 Login</h2>
            <a href="http:127.0.0.1:8000/login">Login with Google</a>

            """


@app.middleware("/http")
async def track_req_per_time(request: Request, call_next):
    print(f"Requst served by {replica}")
    start = time.perf_counter()

    response = await call_next(request)
    duration = time.perf_counter() - start
    logger.info(
        "request completed",
        extra={
            "path": request.url.path,
            "method": request.method,
            "duration": round(duration * 1000, 2),
            "status": response.status_code,
        },
    )
    print(
        f"request completed\nRequst served by {replica}\n{request.method}\n{round(duration * 1000, 2)} ms\n{response.status_code}"
    )

    return response


async def global_exception_handler(request: Request, execption: Exception):
    status_code = 500
    err_message = str(execption)

    if isinstance(execption, StarleteHTTPException):
        status_code = execption.status_code
        err_message = execption.detail

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "data": None,
            "error": err_message,
            "code": status_code,
        },
    )


app.add_exception_handler(StarleteHTTPException, global_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


# import psutil
# import time

# startTime = time.time()


# app.get('/system/performance')
# def performance():
#     return{
#         "cpu_percent":psutil.cpu_percent(),
#         "memory_percent":psutil.virtual_memory().percent,
#         "memory_used_mb":psutil.virtual_memory().used //(1024**2),
#         "uptime_seconds":time.time()-startTime,
#         "active_threads":psutil.Process().num_threads

#     }

request_count = 0
error_count = 0


@app.middleware("http")
async def metrics(request, call_next):
    global request_count, error_count
    request_count += 1

    try:
        response = await call_next(request)
        if response.status_code >= 500:
            error_count += 1
        return response

    except:
        error_count += 1
        raise


@app.get("/metric")
def metrics():
    return {
        "requests": request_count,
        "errors": error_count,
        "error_rate": error_count / request_count if request_count else 0,
    }


client_id = os.getenv("CLIENT_ID")
secret_id = os.getenv("SECRET_ID")
Redirect_URI = os.getenv("Redirect_URI")


Google_Auth_Endpint = "https://accounts.google.com/o/oauth2/auth"
Google_Token_Endpoint = "https://oauth2.googleapis.com/token"
Google_UserInfo_Endpoint = "https://www.googleapis.com/oauth2/v2/userinfo"


@app.get("/login")
def login():
    query_params = {
        "client_id": client_id,
        "redirect_uri": Redirect_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }

    url = f"{Google_Auth_Endpint}?{urlencode(query_params)}"
    return RedirectResponse(url)


@app.get("/auth/callbacks")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": secret_id,
        "redirect_uri": Redirect_URI,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(Google_Token_Endpoint, data=data)
        if token_response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"{token_response}")

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        print(access_token)
        if not access_token:
            raise HTTPException(
                status_code=400, detail="failed to retrieve success token"
            )

        headers = {"Authorization": f"Bearer {access_token}"}
        userinfo_response = await client.get(Google_UserInfo_Endpoint, headers=headers)
        user_info = userinfo_response.json()

        return RedirectResponse(
            f"https://project-arena-iota.vercel.app?name={user_info['name']}&email={user_info['email']}&picture= {user_info['picture']}"
        )


@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    user_info = request.query_params
    name = user_info.get("name")
    email = user_info.get("email")
    picture = user_info.get("picture")

    return f"""
        <html>
            <head><title>User Profile</title></head>
            <body style='text-align:center; font-family:sans-serif'>

            <h1> welcome, {name} </h1>
            <img src="{picture}" alt= "Proflie picture" width="120"/>
            <br>

            <p> Email: {email}</p>
            </body>
        

        
        </html>
    """


import requests
import base64


gh_token = os.getenv("gh_token")

headers = {
    "Authorization": f"Bearer {gh_token}",
}


@app.get("/serve_image", response_class=HTMLResponse)
def getImage():
    response = requests.get(
        "https://raw.githubusercontent.com/wheel-s/carImages/main/audi_2018/2018_A3_2018.webp",
        headers=headers,
    )
    print(response)

    content_type = response.headers.get("Content-Type", "image/octet-stream")
    return StreamingResponse(
        response.iter_content(chunk_size=8192),
        media_type=response.headers.get("Content-Type"),
    )


#       content_type = response.headers.get('Content-Type', 'image/webp')
#     image_data = response.content
#     image_b64 = base64.b64encode(image_data).decode()
#     return f"""
#             <p>yout image</p>
#           <img src="data:{content_type};base64,{image_b64}" alt="Car">
# """
