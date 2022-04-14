import collections.abc
import itertools

from pydantic import BaseModel
from sqlitedict import SqliteDict


class User(BaseModel):
    user_id: int
    user_name: str


users: collections.abc.MutableMapping[int, User] = \
    SqliteDict("data/users.db", tablename="users", autocommit=True)

user_auth: collections.abc.MutableMapping[int, str] = \
    SqliteDict("data/users.db", tablename="user_auth", autocommit=True)


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
