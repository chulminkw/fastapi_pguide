from fastapi import status, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import BlogData
from utils import util
from typing import List
from dotenv import load_dotenv
import os
import time
import aiofiles as aio

load_dotenv()
UPLOAD_DIR = os.getenv("UPLOAD_DIR")


async def get_all_blogs(conn: Connection) -> List:
    try:
        query = """
        SELECT a.id, title, author_id, b.name as author, b.email as email, content, 
        case when image_loc is null then '/static/default/blog_default.png'
             else image_loc end as image_loc
        , modified_dt 
        FROM blog a
          join user b on a.author_id = b.id
        order by modified_dt desc;
        """
        result = await conn.execute(text(query))
        all_blogs = [BlogData(id=row.id,
              title=row.title,
              author_id=row.author_id,
              author=row.author,
              email=row.email,
              content=util.truncate_text(row.content),
              image_loc=row.image_loc, 
              modified_dt=row.modified_dt) for row in result]
    
        result.close()
        return all_blogs
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="알수없는 이유로 서비스 오류가 발생하였습니다")


async def get_blog_by_id(conn: Connection, id: int):
    try:
        query = f"""
        SELECT a.id, title, author_id, b.name as author, b.email as email
        , content, image_loc, modified_dt 
        from blog a
           join user b on a.author_id = b.id
        where a.id = :id
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = await conn.execute(bind_stmt)
        # 만약에 한건도 찾지 못하면 오류를 던진다. 
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")

        row = result.fetchone()
        blog = BlogData(id=row.id, title=row.title, author_id=row.author_id,
                        author=row.author, email=row.email, 
                        content=row.content,
                        image_loc=row.image_loc, modified_dt=row.modified_dt)
        if blog.image_loc is None:
            blog.image_loc = '/static/default/blog_default.png'
        
        result.close()
        return blog
    
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="알수없는 이유로 서비스 오류가 발생하였습니다")

async def upload_file(author: str, imagefile: UploadFile = None):
    try:
        user_dir = f"{UPLOAD_DIR}/{author}/"
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        filename_only, ext = os.path.splitext(imagefile.filename)
        upload_filename = f"{filename_only}_{(int)(time.time())}{ext}"
        upload_image_loc = user_dir + upload_filename

        async with aio.open(upload_image_loc, "wb") as outfile:
            while content := await imagefile.read(1024):
                await outfile.write(content)
        print("upload succeeded:", upload_image_loc)

        return upload_image_loc[1:]
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="이미지 파일이 제대로 Upload되지 않았습니다. ")
  

async def create_blog(conn: Connection, title:str, author_id: int, 
                content:str, image_loc = None):
    try:
        query = f"""
        INSERT INTO blog(title, author_id, content, image_loc, modified_dt)
        values ('{title}', {author_id}, '{content}', {util.none_to_null(image_loc, is_squote=True)} , now())
        """
        
        await conn.execute(text(query))
        await conn.commit()
        
    except SQLAlchemyError as e:
        print(e)
        await conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="요청데이터가 제대로 전달되지 않았습니다.")
    

async def update_blog(conn: Connection,  id: int
                ,  title: str
                , content: str
                , image_loc: str = None):
    
    try:
        query = f"""
        UPDATE blog 
        SET title = :title, content= :content
        , image_loc = :image_loc
        where id = :id
        """
        bind_stmt = text(query).bindparams(id=id, title=title, 
                                           content=content,
                                           image_loc=image_loc)
        result = await conn.execute(bind_stmt)
        # 해당 id로 데이터가 존재하지 않아 update 건수가 없으면 오류를 던진다.
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")
        await conn.commit()
        
    except SQLAlchemyError as e:
        print(e)
        await conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="요청데이터가 제대로 전달되지 않았습니다. ")
    

async def delete_blog(conn: Connection, id: int, image_loc: str = None):
    try:
        query = f"""
        DELETE FROM blog
        where id = :id
        """

        bind_stmt = text(query).bindparams(id=id)
        result = await conn.execute(bind_stmt)
        # 해당 id로 데이터가 존재하지 않아 delete 건수가 없으면 오류를 던진다.
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")
        await conn.commit()

        if image_loc is not None:
            image_path = "." + image_loc
            if os.path.exists(image_path):
                print("image_path:", image_path)
                os.remove(image_path)

    except SQLAlchemyError as e:
        print(e)
        await conn.rollback()
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    except Exception as e:
        print(e)
        await conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="알수없는 이유로 문제가 발생하였습니다. ")

