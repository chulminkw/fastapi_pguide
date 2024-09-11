from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import uuid
import json
import logging

logging.basicConfig(level=logging.CRITICAL) # debugging위해서는 INFO로 변경. 

# Redis setup
redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0, max_connections=10)
redis_client = redis.Redis(connection_pool=redis_pool)

class DummyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("### request info:", request.url, request.method)
        print("### request type:", type(request))

        response = await call_next(request)
        return response
    
class MethodOverrideMiddlware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # print("#### request url, query_params, method", 
        #       request.url, request.query_params, request.method)
        if request.method == "POST":
            query = request.query_params
            if query:
                method_override = query["_method"]
                if method_override:
                    method_override = method_override.upper()
                    if method_override in ("PUT", "DELETE"):
                        request.scope["method"] = method_override
        
        response = await call_next(request)
        return response


class RedisSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, session_cookie: str = "session_redis_id", max_age: int = 3600):
        super().__init__(app)
        self.session_cookie = session_cookie
        self.max_age = max_age

    async def dispatch(self, request: Request, call_next):
        response = None
        # session_id cookie key로 session_id값을 가져옴. 
        session_id = request.cookies.get(self.session_cookie)
        # 신규 session인지 구분. 
        initial_session_was_empty = True
        # 만약 cookie에 session_id 값이 있으면
        if self.max_age is None or self.max_age <= 0:
            response = await call_next(request)
            return response
        try:
            if session_id:
                # redis에서 해당 session_id값으로 저장된 개별 session_data를 가져옴
                session_data = redis_client.get(session_id)
                # redis에 해당 session_id값으로 데이터가 없을 수도 있음. 만약 있다면
                if session_data:
                    # fastapi의 request.state 객체에 새롭게 session 객체를 만들고, 여기에 session data를 저장. 
                    request.state.session = json.loads(session_data)
                    redis_client.expire(session_id, self.max_age)
                    initial_session_was_empty = False
                # 만약 없다면, redis에서 여러 이유로 데이터가 삭제되었음. 
                # request.state.session 객체도 초기화 시키고, 신규 session으로 간주
                else:
                    request.state.session = {}
                    #session_id cookie를 가지고 있지 않다면, 이는 신규 session이고, 추후에 response에 set_cookie 호출. 
                    # new_session = True
            # cookie에 session_id 값이 없다면. 
            else:
                #새로운 session_id값을 uuid로 생성하고 request.state.session값을 초기화.
                # 신규 session으로 간주.  
                session_id = str(uuid.uuid4())
                request.state.session = {}
                # new_session = True

            response = await call_next(request)
            if request.state.session:
                # logging.info("##### request.state.session:" + str(request.state.session))
                # 초기 접속은 물론, 지속적으로 접속하면 max_age를 계속 갱신. 
                response.set_cookie(self.session_cookie, session_id, max_age=self.max_age, httponly=True)
                # redis에서 해당 session_id를 가지는 값을 set 저장. 
                # request.state.session값의 변경 여부와 관계없이 저장
                # expiration time을 지속적으로 max_age로 갱신. 
                redis_client.setex(session_id, self.max_age, json.dumps(request.state.session))
                
            else:
                # request.state.session가 비어있는데, initial_session_was_empty가 False라는 것은
                # fastapi API 로직에서 request.state.session이 clear() 호출되어서 삭제되었음을 의미. 
                # logout이므로 redis에서 해당 session_id 값을 삭제하고, 브라우저의 cookie도 삭제. 
                if not initial_session_was_empty:
                    # logging.info("##### redis value before deletion:" + str(redis_client.get(session_id)))
                    redis_client.delete(session_id)
                    # logging.info("##### redis value after deletion:" + str(redis_client.get(session_id)))
                    response.delete_cookie(self.session_cookie)
        except Exception as e:
            logging.critical("error in redis session middleware:" + str(e))
        
        return response
                
        