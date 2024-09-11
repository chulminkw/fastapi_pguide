from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# jinja2 Template 생성. 인자로 directory 입력
templates = Jinja2Templates(directory="templates")


class Item(BaseModel):
    name: str
    description: str

@app.get("/all_items", response_class=HTMLResponse)
async def read_all_items(request: Request):
    all_items = [Item(name="테스트_상품명_" +str(i), 
                      description="테스트 내용입니다. 인덱스는 " + str(i)) for i in range(5) ]
    print("all_items:", all_items)
    return templates.TemplateResponse(
        request=request, 
        name="index_no_include.html",
        #name="index_include.html",
        #name="index.html", 
        context={"all_items": all_items}
    )