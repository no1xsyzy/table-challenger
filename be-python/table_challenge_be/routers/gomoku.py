from fastapi import APIRouter, HTTPException

from ..internal import gomoku
from ..internal import users

router = APIRouter()


@router.get("/gomoku")
def hello_gomoku():
    return {'hello': 'gomoku'}


@router.post("/gomoku/table")
def create_table(tablepass: str) -> int:
    return gomoku.create_table(tablepass)


@router.get("/obSv701/all_tables")
def observe_tables():
    return gomoku.table_passes


@router.get("/gomoku/table/{table_id}")
def see_table(table_id: int, tablepass: str, uid: int, userpass: str) -> gomoku.GomokuTableStatus:
    if not gomoku.check_table(table_id, tablepass):
        raise HTTPException(status_code=404, detail='not table')
    if users.check_user(uid, userpass):
        gomoku.heartbeat(table_id, uid)
    p1, p2, left_is_black = gomoku.table_dueler[table_id]
    return gomoku.GomokuTableStatus(
        table_id=table_id,
        state=gomoku.table_state[table_id],
        player1=users.users.get(p1),
        player2=users.users.get(p2),
        left_is_black=left_is_black,
        queue=[users.users[uid] for uid in gomoku.table_queue[table_id]],
        moves=[gomoku.Move(x=x, y=y) for x, y in gomoku.table_moves[table_id]]
    )


@router.post("/gomoku/table/{table_id}/queue")
def enter_queue(table_id: int, tablepass: str, uid: int, userpass: str) -> str:
    if not users.check_user(uid, userpass):
        return 'not user'
    if not gomoku.check_table(table_id, tablepass):
        return 'not table'
    p1, p2, lb = gomoku.table_dueler[table_id]
    if uid == p1 or uid == p2 or uid in gomoku.table_queue[table_id]:
        return 'already in queue'
    if p1 == 0:
        gomoku.table_dueler[table_id] = uid, p2, lb
        state = gomoku.table_state[table_id]
        new_state = gomoku.seat_map.get((state, 1))
        if new_state is None:
            return 'unknown error'

        gomoku.table_state[table_id] = new_state
    elif p2 == 0:
        gomoku.table_dueler[table_id] = p1, uid, lb
        state = gomoku.table_state[table_id]
        new_state = gomoku.seat_map.get((state, 2))
        if new_state is None:
            return 'unknown error'
        gomoku.table_state[table_id] = new_state
    else:
        gomoku.table_queue[table_id] = [*gomoku.table_queue[table_id], uid]
    return 'success'


@router.post("/gomoku/table/{table_id}/ready")
def player_ready(table_id: int, tablepass: str, uid: int, userpass: str) -> str:
    if not users.check_user(uid, userpass):
        return 'not user'
    if not gomoku.check_table(table_id, tablepass):
        return 'not table'
    p1, p2, lb = gomoku.table_dueler[table_id]
    if uid not in [p1, p2]:
        return 'not dueler'
    state = gomoku.table_state[table_id]
    rr = 1 if uid == p1 else 2 if uid == p2 else 0
    next_state = gomoku.ready_map.get((state, rr))
    if next_state is None:
        return 'cannot ready'
    if next_state == gomoku.TableState.PLAYING:
        gomoku.start_game(table_id)
    elif state == gomoku.TableState.C_P1W:
        gomoku.kick_user(table_id, 2)
    elif state == gomoku.TableState.C_P2W:
        gomoku.kick_user(table_id, 1)
    else:
        gomoku.table_state[table_id] = next_state
    return 'ready'


@router.post("/gomoku/table/{table_id}/move")
def do_move(table_id: int, tablepass: str,
            uid: int, userpass: str,
            move: gomoku.Move) -> str:
    if not users.check_user(uid, userpass):
        return 'not user'
    if not gomoku.check_table(table_id, tablepass):
        return 'not table'
    if not gomoku.table_state[table_id] == gomoku.TableState.PLAYING:
        return 'not playing'
    p1, p2, lb = gomoku.table_dueler[table_id]
    if uid not in [p1, p2]:
        return 'not dueler'
    last_mover_black = len(gomoku.table_moves[table_id]) % 2 == 1
    if ((uid == p1) + lb + last_mover_black) % 2 == 1:
        return 'not round'
    # uid | lb | lmb | round?
    # p1  | T  | T   | F
    print(move)
    gomoku.table_moves[table_id] = [*gomoku.table_moves[table_id], (move.x, move.y)]
    print(gomoku.table_moves[table_id])
    winner = gomoku.check_winner(table_id)
    if (winner == 'black' and lb) or (winner == 'white' and not lb):
        gomoku.table_state[table_id] = gomoku.TableState.C_P1W
        return 'P1 win'
    if (winner == 'white' and lb) or (winner == 'black' and not lb):
        gomoku.table_state[table_id] = gomoku.TableState.C_P2W
        return 'P2 win'
    return 'done'
