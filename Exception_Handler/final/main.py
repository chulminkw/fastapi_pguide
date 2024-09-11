from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from routes import blog
from db.database import engine
from utils.common import lifespan
from utils import exc_handler

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(blog.router)

app.add_exception_handler(StarletteHTTPException, exc_handler.custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, exc_handler.validation_exception_handler)