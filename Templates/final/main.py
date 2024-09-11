from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# jinja2 Template 생성. 인자로 directory 입력
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str
    price: float

# response_class=HTMLResponse를 생략하면 application/json으로 Swagger UI에서 인식(별 문제는 없음)
@app.get("/items/{id}", response_class=HTMLResponse)
# template engine을 사용할 경우 반드시 Request 객체가 인자로 입력되어야 함. 
async def read_item(request: Request, id: str, q: str | None = None):
    # 내부에서 pydantic 객체 생성. 
    item = Item(
        name="test_item", 
        price=10
    )
    # pydantic model값을 dict 변환. 
    item_dict = item.model_dump()
    
    return templates.TemplateResponse(
        request=request, 
        name="item.html", 
        context={"id": id, "q_str": q, "item": item, "item_dict": item_dict}
    )
    # FastAPI 0.108 이하 버전에서는 아래와 같이 TemplateResponse() 인자 호출
    # return templates.TemplateResponse(name="item.html",
    #                                   {"request": request
    #                                    , "id": id, "q_str": q, "item": item, "item_dict": item_dict})


@app.get("/item_gubun")
async def read_item_by_gubun(request: Request, gubun: str):
    item = Item(name="test_item_02", price=4.0)
    
    return templates.TemplateResponse(
        request=request, 
        name="item_gubun.html", 
        context={"gubun": gubun, "item": item}
    )

@app.get("/all_items", response_class=HTMLResponse)
async def read_all_items(request: Request):
    all_items = [Item(name="test_item_" +str(i), price=i) for i in range(5) ]
    print("all_items:", all_items)
    return templates.TemplateResponse(
        request=request, 
        name="item_all.html", 
        context={"all_items": all_items}
    )

@app.get("/read_safe", response_class=HTMLResponse)
async def read_safe(request: Request):
    html_str = '''
    <ul>
    <li>튼튼</li>
    <li>저렴</li>
    </ul>
    '''
    return templates.TemplateResponse(
        request=request, 
        name="read_safe.html", 
        context={"html_str": html_str}
    )
