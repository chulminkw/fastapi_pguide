from fastapi import FastAPI
from enum import Enum

app = FastAPI()

#http://localhost:8081/items/3
# decorator에 path값으로 들어오는 문자열중에 
# format string { }로 지정된 변수가 path parameter
@app.get("/items/{item_id}")
# 수행 함수 인자로 path parameter가 입력됨. 
# 함수 인자의 타입을 지정하여 path parameter 타입 지정. 
async def read_item(item_id: int):
    return {"item_id": item_id}

# Path parameter값과 특정 지정 Path가 충돌되지 않도록 endpoint 작성 코드 위치에 주의 
@app.get("/items/all")
# 수행 함수 인자로 path parameter가 입력됨. 함수 인자의 타입을 지정하여 path parameter 타입 지정.  
async def read_all_items():
    return {"message": "all items"}

# Path parameter에 지정된 특정 값들만 원할 때는 아래와 같이 Enum Class로 Path유형을 지정. 
# Enum class를 enum mixin으로 str을 확장하는 class로 만듬. 
class ItemType(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"

#item_type의 값으로 small/medium/large만 가능. 
@app.get("/items/type/{item_type}")
async def get_item_type(item_type: ItemType):
    return {"message": f"item type is {item_type}"}

# @app.get("/items/type/{item_type}")
# async def get_item_type(item_type: ItemType):
#     if item_type is ItemType.small:
#          return {"message": f"small item type should be very small {item_type}"}
    
#     return {"message": f"item type is {item_type}"}


