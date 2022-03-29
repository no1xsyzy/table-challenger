from fastapi import APIRouter, HTTPException

from ..internal import users

router = APIRouter()


@router.post("/users")
def register(userpass: str) -> int:
    return users.create_user(userpass)


@router.post("/users/login")
def login(uid: int, userpass: str) -> users.User:
    if uid in users.user_auth and users.user_auth[uid] == userpass:
        return users.users[uid]
    raise HTTPException(status_code=404, detail="not user")


@router.get("/users/{uid}")
def see_user(uid: int) -> users.User:
    try:
        return users.users[uid]
    except KeyError:
        raise HTTPException(status_code=404, detail="not user")


@router.put("/users/{uid}/name")
def rename(uid: int, userpass: str, name: str):
    if not users.check_user(uid, userpass):
        return HTTPException(status_code=404, detail="not user")
    users.users[uid].user_name = name
