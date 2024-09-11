from fastapi import status
from fastapi.exceptions import HTTPException
from schemas.auth_schema import UserData, UserDataPASS
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from utils import util
from typing import List
from dotenv import load_dotenv
import os
import time
 
async def get_user_by_email(conn: Connection, email: str) -> UserData:
    try:
        query = f"""
        SELECT id, name, email from user
        where email = :email
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(email=email)
        result = await conn.execute(bind_stmt)
        # 만약에 한건도 찾지 못하면 None을 던진다. 
        if result.rowcount == 0:
            return None

        row = result.fetchone()
        user = UserData(id=row[0], name=row[1], email=row[2])
        
        result.close()
        return user
    
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="알수없는 이유로 서비스 오류가 발생하였습니다")
    
async def get_userpass_by_email(conn: Connection, email: str) -> UserDataPASS:
    try:
        query = f"""
        SELECT id, name, email, hashed_password from user
        where email = :email
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(email=email)
        result = await conn.execute(bind_stmt)
        # 만약에 한건도 찾지 못하면 None을 던진다. 
        if result.rowcount == 0:
            return None

        row = result.fetchone()
        userpass = UserDataPASS(id=row[0], name=row[1], email=row[2]
                            , hashed_password=row[3])
        
        result.close()
        return userpass
    
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="알수없는 이유로 서비스 오류가 발생하였습니다")


async def register_user(conn: Connection, name: str, email:str, hashed_password: str):
    try:
        query = f"""
        INSERT INTO user(name, email, hashed_password)
        values ('{name}', '{email}', '{hashed_password}')        
        """
        print("query:", query)
        await conn.execute(text(query))
        await conn.commit()
        
    except SQLAlchemyError as e:
        print(e)
        await conn.rollback()
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    
# async def register_user_check()