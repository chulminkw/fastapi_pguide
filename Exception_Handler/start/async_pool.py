from sqlalchemy import text
from db.database import direct_get_conn, engine
import asyncio

async def execute_sleep_query():
    for ind in range(10):
        print("loop index:", ind)
        conn = await direct_get_conn()
        query = "select sleep(5)"
        stmt = text(query)
        result = await conn.execute(stmt)
        await conn.close()
    await engine.dispose()

async def main():
    await execute_sleep_query()

if __name__ == "__main__":
   asyncio.run(main())



    
    




