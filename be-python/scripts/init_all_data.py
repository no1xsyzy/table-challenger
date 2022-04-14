#!/usr/bin/env python

from table_challenge_be.internal.users import users, user_auth, User
from table_challenge_be.internal.gomoku import table_passes, table_state, table_dueler, table_queue, table_moves, table_user_heartbeat

users.clear()
users[1] = User(user_id=1, user_name='user1')
users[2] = User(user_id=2, user_name='user2')
users[3] = User(user_id=3, user_name='user3')
users[4] = User(user_id=4, user_name='user4')

user_auth.clear()
user_auth[1] = "aa"
user_auth[2] = "bb"
user_auth[3] = "cc"
user_auth[4] = "dd"

table_passes.clear()
table_state.clear()
table_dueler.clear()
table_queue.clear()
table_moves.clear()
table_user_heartbeat.clear()
