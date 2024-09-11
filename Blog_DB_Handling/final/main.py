from fastapi import FastAPI
from routes import blog

app = FastAPI()
app.include_router(blog.router)
