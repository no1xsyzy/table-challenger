import collections.abc
import itertools
import random
import typing
from collections import deque
from datetime import datetime, timedelta

from sqlitedict import SqliteDict

from ..models.gomoku import TableState, GomokuTableStatus, Move

__all__ = (
    'TableState', 'GomokuTableStatus', 'Move',
    'table_passes',
    'table_state',
    'table_dueler',
    'table_queue',
    'table_moves',
    'table_user_heartbeat',
)

seat_map: dict[tuple[TableState, int], TableState] = {
    (TableState.IDLE, 1): TableState.P1S,
    (TableState.IDLE, 2): TableState.P2S,
    (TableState.P1S, 2): TableState.BS,
    (TableState.P2S, 1): TableState.BS,
    (TableState.C_P1W, 2): TableState.BS,
    (TableState.C_P2W, 1): TableState.BS,
}

ready_map: dict[tuple[TableState, int], TableState] = {
    (TableState.BS, 1): TableState.BS_P1R,
    (TableState.BS, 2): TableState.BS_P2R,
    (TableState.BS_P1R, 2): TableState.PLAYING,
    (TableState.BS_P2R, 1): TableState.PLAYING,
    (TableState.C_P1W, 1): TableState.BS_P1R,
    (TableState.C_P2W, 2): TableState.BS_P2R,
}

table_passes: collections.abc.MutableMapping[int, str] = \
    SqliteDict("data/gomoku.db", tablename="table_passes", autocommit=True)
table_state: collections.abc.MutableMapping[int, TableState] = \
    SqliteDict("data/gomoku.db", tablename="table_state", autocommit=True)
table_dueler: collections.abc.MutableMapping[int, tuple[int, int, bool]] = \
    SqliteDict("data/gomoku.db", tablename="table_dueler", autocommit=True)
table_queue: collections.abc.MutableMapping[int, list[int]] = \
    SqliteDict("data/gomoku.db", tablename="table_queue", autocommit=True)
table_moves: collections.abc.MutableMapping[int, list[tuple[int, int]]] = \
    SqliteDict("data/gomoku.db", tablename="table_moves", autocommit=True)

table_user_heartbeat: collections.abc.MutableMapping[str, datetime] = \
    SqliteDict("data/gomoku.db", tablename="table_user_heartbeat", autocommit=True)


def heartbeat(table_id, user_id):
    table_user_heartbeat[f"{table_id},{user_id}"] = datetime.now()


def clean_dead():
    death = datetime.now() - timedelta(seconds=10)
    cleaned = []
    for (tuid, beat) in table_user_heartbeat.items():
        if beat < death:
            table_id, user_id = map(int, tuid.split(","))
            cleaned.append(tuid)
            if user_id in table_queue[table_id]:
                table_queue[table_id] = [m for m in table_queue[table_id] if m != user_id]
            elif user_id in (dueler := table_dueler[table_id]):
                pass
                # TODO: dead user auto lose
    for clean in cleaned:
        del table_user_heartbeat[clean]


def find_free_table_id():
    for i in itertools.count(1):
        if i not in table_passes:
            return i


def create_table(tablepass: str):
    table_id = find_free_table_id()
    table_passes[table_id] = tablepass
    table_state[table_id] = TableState.IDLE
    table_dueler[table_id] = (0, 0, False)
    table_queue[table_id] = []
    table_moves[table_id] = []
    return table_id


def construct_face(moves: list[Move]) -> list[list[int]]:
    face = [[0] * 15 for _ in range(15)]
    black = True
    for move in moves:
        face[move.x][move.y] = 1 if black else 2
        black = not black
    return face


def start_game(table_id: int):
    table_state[table_id] = TableState.PLAYING
    p1, p2, lb = table_dueler[table_id]
    lb = random.choice((True, False))
    table_dueler[table_id] = p1, p2, lb
    table_moves[table_id] = []


def check_winner(table_id: int) -> typing.Literal['black', 'white', '']:
    face = construct_face([Move(x=x, y=y) for x, y in table_moves[table_id]])
    for cl_func in [
        construct_lines_vvec,
        construct_lines_hvec,
        construct_lines_md,
        construct_lines_sd,
    ]:
        for line in cl_func(face):
            check = check_line(line)
            if check:
                return check
    return ''


def construct_lines_vvec(face) -> typing.Iterable[typing.Iterable[int]]:
    return [v[:] for v in face]


def construct_lines_hvec(face) -> typing.Iterable[typing.Iterable[int]]:
    return zip(*face)


def construct_lines_md(face) -> typing.Iterable[typing.Iterable[int]]:
    return ((face[t][t + d] for t in range(15 - abs(d))) for d in range(-10, 11))


def construct_lines_sd(face) -> typing.Iterable[typing.Iterable[int]]:
    return ((face[x][s - x] for x in (range(0, s + 1) if s <= 14 else range(s - 14, 15))) for s in range(4, 25))


def check_line(line: typing.Iterable[int]) -> typing.Literal['black', 'white', '']:
    window = deque([], 5)
    for s in line:
        window.append(s)
        if list(window) == [1] * 5:
            return 'black'
        elif list(window) == [2] * 5:
            return 'white'
    return ''


def check_table(table_id: int, passphrase: str):
    return table_id in table_passes and passphrase == table_passes[table_id]


def kick_user(table_id: int, pos: int):
    if pos == 1:
        p1, p2, lb = table_dueler[table_id]
        np1 = 0
        if table_queue[table_id]:
            np1, *table_queue[table_id] = table_queue[table_id]
        table_dueler[table_id] = np1, p2, lb
        table_state[table_id] = calculate_seat(np1, p2)
        table_moves[table_id] = []
    elif pos == 2:
        p1, p2, lb = table_dueler[table_id]
        np2 = 0
        if table_queue[table_id]:
            np2, *table_queue[table_id] = table_queue[table_id]
        table_dueler[table_id] = p1, np2, lb
        table_state[table_id] = calculate_seat(p1, np2)
        table_moves[table_id] = []


def calculate_seat(p1, p2) -> TableState:
    if p1 == 0:
        if p2 == 0:
            return TableState.IDLE
        else:
            return TableState.P2S
    else:
        if p2 == 0:
            return TableState.P1S
        else:
            return TableState.BS
