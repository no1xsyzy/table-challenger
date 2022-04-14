#!/usr/bin/env python

from table_challenge_be.internal.users import users, user_auth, User

users[1] = User(user_id=1, user_name='user1')
users[2] = User(user_id=2, user_name='user2')
users[3] = User(user_id=3, user_name='user3')
users[4] = User(user_id=4, user_name='user4')
user_auth[1] = "aa"
user_auth[2] = "bb"
user_auth[3] = "cc"
user_auth[4] = "dd"
