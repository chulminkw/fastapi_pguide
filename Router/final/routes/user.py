from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def read_users():
    return [{"username": "Rickie"}, {"username": "Martin"}]

@router.get("/me")
async def read_user_me():
    return {"username": "currentuser"}

@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}