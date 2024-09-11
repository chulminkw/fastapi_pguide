from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import blog

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(blog.router)
