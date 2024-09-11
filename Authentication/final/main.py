from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from routes import blog, auth
from utils.common import lifespan
from utils import exc_handler, middleware

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(CORSMiddleware, 
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   allow_credentials=True,
                   max_age=-1)
# app.add_middleware(middleware.DummyMiddleware)
app.add_middleware(middleware.MethodOverrideMiddlware)

app.include_router(blog.router)
app.include_router(auth.router)

app.add_exception_handler(StarletteHTTPException, exc_handler.custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, exc_handler.validation_exception_handler)