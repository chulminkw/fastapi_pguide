import redis

#localhost, post=6379, db=0으로 접속 (default port is 6379) and use database 0
r_client = redis.Redis(host='localhost', port=6379, db=0)

# db=0 key와 value 설정한 뒤 해당 key값으로 값 추출. 
r_client.set('name', 'FastAPI')
name_value = r_client.get('name')
print(f"Value for 'name' in db 0: {name_value.decode('utf-8')}")

# db1에 접속
r_client_db1 = redis.Redis(host='localhost', port=6379, db=1)

# db=1 key와 value 설정한 뒤 해당 key값으로 값 추출. 
r_client_db1.set('name', 'Redis')
name_value_db1 = r_client_db1.get('name')
print(f"Value for 'name' in db 1: {name_value_db1.decode('utf-8')}")

# Connection Pool 기반 access
redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0, max_connections=10)
redis_client_pool = redis.Redis(connection_pool=redis_pool)

redis_client_pool.set('name', 'FastAPI')
name_value = redis_client_pool.get('name')
print(f"Value for 'name' in db 0: {name_value.decode('utf-8')}")