import itertools

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    user_name: str


# users: dict[int, User] = {}
# user_auth: dict[int, str] = {}

users: dict[int, User] = {
    1: User(user_id=1, user_name='user1'),
    2: User(user_id=2, user_name='user2'),
    3: User(user_id=3, user_name='user3'),
    4: User(user_id=4, user_name='user4'),
}
user_auth: dict[int, str] = {
    1: "aa",
    2: "bb",
    3: "cc",
    4: "dd",
}


def check_user(user_id: int, password: str):
    return user_auth.get(user_id) == password


def find_free_user_id():
    for i in itertools.count(1):
        if i not in users:
            return i


def create_user(userpass: str) -> int:
    uid = find_free_user_id()
    user_auth[uid] = userpass
    users[uid] = User(user_id=uid, user_name=f"user{uid}")
    return uid
