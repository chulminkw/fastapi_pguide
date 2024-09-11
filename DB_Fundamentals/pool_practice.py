from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool

# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"

# engine = create_engine(DATABASE_CONN)
engine = create_engine(DATABASE_CONN, 
                       poolclass=QueuePool,
                       #poolclass=NullPool, # Connection Pool 사용하지 않음. 
                       pool_size=10, max_overflow=2
                       )
print("#### engine created")

def direct_execute_sleep(is_close: bool = False):
    conn = engine.connect()
    query = "select sleep(5)"
    result = conn.execute(text(query))
    # rows = result.fetchall()
    # print(rows)
    result.close()

    # 인자로 is_close가 True일 때만 connection close()
    if is_close:
        conn.close()
        print("conn closed")

for ind in range(20):
    print("loop index:", ind)
    direct_execute_sleep(is_close=True)


print("end of loop")

    
