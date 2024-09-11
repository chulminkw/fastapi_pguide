from fastapi import (
    FastAPI, Request, Depends, HTTPException, 
    Form, Response, Cookie, status
)
from fastapi.responses import HTMLResponse, RedirectResponse
import json

app = FastAPI()

# 테스트용 User를 Dict로 생성. 
users_db = {
    "gildong@gmail.com": {
        "username":"gildong",
        "email":"gildong@gmail.com",
        "password":"fastapi"
    }
}

# Request 객체에서 cookie 정보 추출 
def get_logged_user(request: Request):
    cookies = request.cookies
    print("cookies:", cookies)
    if "my_cookie" in cookies.keys():
        my_cookie_value = cookies["my_cookie"]
        cookie_user = json.loads(my_cookie_value)
        print("cookie_user:", cookie_user)
        return cookie_user
    
    return None
# Cookie 클래스를 이용하여 cookie 정보 추출
def get_logged_user_by_cookie_di(my_cookie=Cookie(None)):
    if not my_cookie:
        return None
    
    cookie_user = json.loads(my_cookie)
    print("cookie_user:", cookie_user)
    return cookie_user

# Home page
@app.get("/")
async def read_root(cookie_user: dict = Depends(get_logged_user_by_cookie_di)):
    if not cookie_user:
        return HTMLResponse("로그인 하지 않았습니다. 여기서 로그인 해주세요. <a href='/login'> 로그인 </a>",
                            status_code=status.HTTP_401_UNAUTHORIZED)
    return HTMLResponse(f"환영합니다. {cookie_user['username']}님")

# Login UI page
@app.get("/login")
async def login_form():
    return HTMLResponse("""
    <form action="/login" method="post">
        Email: <input type="email" name="email"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    """)

# login 수행.
@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    
    user_data = users_db[email]
     
    # DB에 있는 email/password가 Form으로 입력 받은 email/password가 다를 경우 HTTPException 발생.
    if not user_data  or user_data["password"] != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Email과 Password가 일치하지 않습니다")

    # FastAPI의 Response 객체에 cookie 값 설정. 
    user_json = json.dumps({"username": user_data["username"],
                "email": user_data["email"]})
    
    # 반드시 return되는 response 객체에 set_cookie()를 호출해서 쿠키전달
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    # set_cookie()의 max_age 인자가 안들어가면 Session Cookie임.
    # expires와 max_age 중에 하나 선택. 두개 다 있으면 max_age를 선택함.
    # 기본 httponly=True, samesite=Lax
    response.set_cookie(key="my_cookie", value=user_json, httponly=True, max_age=3600)
    #response.set_cookie(key="my_another_cookie", value=user_json, httponly=True, max_age=3600)

    return response

@app.get("/user_profile")
async def user_profile(cookie_user: dict = Depends(get_logged_user_by_cookie_di)):
    if not cookie_user:
        return HTMLResponse("로그인 하지 않았습니다. 여기서 로그인 해주세요. <a href='/login'>로그인</a>.", 
                            status_code=status.HTTP_401_UNAUTHORIZED)
    return HTMLResponse(f"{cookie_user['username']}님의 email 주소는 {cookie_user['email']}")

@app.get("/logout")
async def logout(response: Response):
    # Cookie를 삭제함. 
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("my_cookie")
    return response


