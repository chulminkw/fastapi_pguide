from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/item", tags=["item"])

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@router.get("/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@router.post("/")
async def create_item(item: Item):
    return item

@router.put("/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}