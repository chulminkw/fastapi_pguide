from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import blog
from contextlib import asynccontextmanager
from db.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # FastAPI 인스턴스 기동시 필요한 작업 수행. 
    print("Starting up...")
    yield

    #FastAPI 인스턴스 종료시 필요한 작업 수행
    print("Shutting down...")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(blog.router)

