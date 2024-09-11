from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from db.database import direct_get_conn, context_get_conn
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import Blog, BlogData
from services import blog_svc
from utils import util
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler

# router 생성
router = APIRouter(prefix="/blogs", tags=["blogs"])
# jinja2 Template 엔진 생성
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_all_blogs(request: Request, conn: Connection = Depends(context_get_conn)):
    all_blogs = await blog_svc.get_all_blogs(conn)
    
    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {"all_blogs": all_blogs}
    )
    
@router.get("/show/{id}")
async def get_blog_by_id(request: Request, id: int,
                   conn: Connection = Depends(context_get_conn)):
    blog = await blog_svc.get_blog_by_id(conn, id)
    blog.content = util.newline_to_br(blog.content)

    return templates.TemplateResponse(
        request = request,
        name="show_blog.html",
        context = {"blog": blog})
 
@router.get("/new")
async def create_blog_ui(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "new_blog.html",
        context = {}
    )

@router.post("/new")
async def create_blog(request: Request
                , title = Form(min_length=2, max_length=200)
                , author = Form(max_length=100)
                , content = Form(min_length=2, max_length=4000)
                , imagefile: UploadFile | None = File(None)
                , conn: Connection = Depends(context_get_conn)):
    # print("##### imagefile:", imagefile)
    # print("#### filename:", imagefile.filename)
    image_loc = None
    if len(imagefile.filename.strip()) > 0:
        # 반드시 transactional 한 처리를 위해 upload_file()이 먼저 수행되어야 함.
        image_loc = await blog_svc.upload_file(author=author, imagefile=imagefile)
        await blog_svc.create_blog(conn, title=title, author=author
                         , content=content, image_loc=image_loc)
    else:
        await blog_svc.create_blog(conn, title=title, author=author
                         , content=content, image_loc=image_loc)


    return RedirectResponse("/blogs", status_code=status.HTTP_302_FOUND)
    

@router.get("/modify/{id}")
async def update_blog_ui(request: Request, id: int, conn = Depends(context_get_conn)):
    blog = await blog_svc.get_blog_by_id(conn, id=id)
    
    return templates.TemplateResponse(
        request = request,
        name="modify_blog.html",
        context = {"blog": blog}
    )
    
@router.post("/modify/{id}")
async def update_blog(request: Request, id: int
                , title = Form(min_length=2, max_length=200)
                , author = Form(max_length=100)
                , content = Form(min_length=2, max_length=4000)
                , imagefile: UploadFile | None = File(None)
                , conn: Connection = Depends(context_get_conn)):
    image_loc = None
    if len(imagefile.filename.strip()) > 0:
        image_loc = await blog_svc.upload_file(author=author, imagefile=imagefile)
        await blog_svc.update_blog(conn=conn, id=id, title=title, author=author
                             , content=content, image_loc = image_loc)
    else:
        await blog_svc.update_blog(conn=conn, id=id, title=title, author=author
                             , content=content, image_loc = image_loc)

    return RedirectResponse(f"/blogs/show/{id}", status_code=status.HTTP_302_FOUND)
    
@router.delete("/delete/{id}")
async def delete_blog(request: Request, id: int
                , conn: Connection = Depends(context_get_conn)):
    blog = await blog_svc.get_blog_by_id(conn=conn, id=id)
    await blog_svc.delete_blog(conn=conn, id=id, image_loc=blog.image_loc)
    return JSONResponse(content="메시지가 삭제되었습니다", status_code=status.HTTP_200_OK)
    # return RedirectResponse("/blogs", status_code=status.HTTP_302_FOUND)