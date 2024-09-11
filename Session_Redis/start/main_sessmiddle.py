from fastapi import FastAPI, Request, Depends, HTTPException, Form, status
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os

app = FastAPI()

# SessionMiddleware의 secret_key 값 생성. 
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# SessionMiddleware 등록
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, max_age=3600)

# 테스트용 User를 Dict로 생성. 
users_db = {
    "gildong@gmail.com": {
        "username":"gildong",
        "email":"gildong@gmail.com",
        "password":"fastapi"
    }
}

def get_session(request: Request):
    print("request.session:", request.session)
    return request.session

def get_session_user(request: Request):
    session = request.session
    if "session_user" not in session.keys():
        return None
    else:
        session_user = session["session_user"]
        return session_user

@app.get("/")
async def read_root(request: Request, session_user: dict = Depends(get_session_user)):
    if not session_user:
        return HTMLResponse("로그인 하지 않았습니다. 여기서 로그인 해주세요. <a href='/login'>로그인</a>.", 
                            status_code=status.HTTP_401_UNAUTHORIZED)
    return HTMLResponse(f"환영합니다. {session_user['username']}님")

@app.get("/login")
async def login_form():
    # Simple login form
    return HTMLResponse("""
    <form action="/login" method="post">
        Email: <input type="email" name="email"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    """)

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user_data = users_db.get(email)
    # DB에 있는 email/password가 Form으로 입력 받은 email/password가 다를 경우 HTTPException 발생.
    if not user_data or user_data["password"] != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Email과 Password가 일치하지 않습니다")

    # FastAPI의 Response 객체에 signed cookie 값 설정. 
    session = request.session
    session["session_user"] = {"username": user_data["username"], "email": user_data["email"]}
    
    # response 객체에 set_cookie()를 호출하지 않아야 함. 자동으로 cookie값 설정됨. 
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()  # session clear
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@app.get("/user_profile")
async def user_profile(session_user: dict = Depends(get_session_user)):
    if not session_user:
        return HTMLResponse("로그인 하지 않았습니다. 여기서 로그인 해주세요. <a href='/login'>로그인</a>.", 
                            status_code=status.HTTP_401_UNAUTHORIZED)
    
    return HTMLResponse(f"{session_user['username']}님의 email 주소는 {session_user['email']}")