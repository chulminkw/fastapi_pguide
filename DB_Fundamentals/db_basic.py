from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@127.0.0.1:3306/blog_db"
# Engine 생성
engine = create_engine(DATABASE_CONN, poolclass=QueuePool,
             pool_size=10, max_overflow=0)

try: 
    # Connection 얻기
    conn = engine.connect()
    # SQL 선언 및 text로 감싸기
    query = "select id, title from blog"
    stmt = text(query)
    
    # SQL 호출하여 CursorResult 반환.
    result = conn.execute(stmt)
    print("type result:", result)

    rows = result.fetchall()
    print(rows)

    # print(type(rows[0]))
    # print(rows[0].id, rows[0].title)
    # print(rows[0][0], rows[0][1])
    # print(rows[0]._key_to_index)

    result.close()
except SQLAlchemyError as e:
    print(e)
finally: 
    # close() 메소드 호출하여 connection 반환.
    conn.close()
