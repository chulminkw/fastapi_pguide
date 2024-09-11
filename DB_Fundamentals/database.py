from sqlalchemy import create_engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import contextmanager


# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"

engine = create_engine(DATABASE_CONN,
                       poolclass=QueuePool,
                       #poolclass=NullPool, # Connection Pool 사용하지 않음. 
                       pool_size=10, max_overflow=0)

def direct_get_conn():
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise e

#with 절 사용시 이슈 
# def context_get_conn():
#     try:
#         with engine.connect() as conn:
#             yield conn
#     except SQLAlchemyError as e:
#         print(e)
#         raise e
#     finally:
#         conn.close()
#         print("###### connection yield is finished")
  
@contextmanager
def context_get_conn():
    try:
        conn = engine.connect()
        yield conn
    except SQLAlchemyError as e:
        print(e)
        raise e
    finally: 
        conn.close()
    

    