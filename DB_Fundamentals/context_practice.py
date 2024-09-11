from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool

# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"

engine = create_engine(DATABASE_CONN,
                       poolclass=QueuePool,
                       #poolclass=NullPool,
                       pool_size=10, max_overflow=0)

def context_execute_sleep():
    with engine.connect() as conn:
        query = "select sleep(5)"
        result = conn.execute(text(query))
        result.close()
        #conn.close()

for ind in range(20):
    print("loop index:", ind)
    context_execute_sleep()

print("end of loop")