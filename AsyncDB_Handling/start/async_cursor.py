from sqlalchemy import text
from db.database import direct_get_conn, engine
import asyncio


async def execute_query():
    conn = await direct_get_conn()
    query = "select * from blog"
    stmt = text(query)
    # SQL 호출하여 CursorResult 반환. 
    result = await conn.execute(stmt)
    # 아래는 오류를 발생. 
    rows = await result.fetchone()
    print(rows)
    result.close()
    await conn.rollback()
    await conn.close()
    await engine.dispose()

async def stream_query():
    conn = await direct_get_conn()
    query = "select * from blog"
    stmt = text(query)
    # connection의 execute()가 아닌 stream()을 호출해야 함. 
    async_result = await conn.stream(stmt)
    # async로 iteration 수행. 
    async for row in async_result:
        print(row)

    await async_result.close()
    await conn.rollback()
    await conn.close()
    await engine.dispose()

async def main():
    await stream_query()
    #await execute_query()

if __name__ == "__main__":
    asyncio.run(main())