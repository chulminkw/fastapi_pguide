from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/item")
async def create_item(item: Item):
    return item

@app.put("/item/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

@app.get("/users/")
async def read_users():
    return [{"username": "Rickie"}, {"username": "Martin"}]


@app.get("/users/me")
async def read_user_me():
    return {"username": "currentuser"}


@app.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}