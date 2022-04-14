import { API_HOST } from './API_HOST'
import type { Move, User, GomokuTableStatus } from './types/gomoku'
export type { Move, User, GomokuTableStatus }

export enum TableState {
  IDLE = 0,
  P1S = 1,
  P2S = 2,
  BS = 100,
  P1R = 101,
  P2R = 102,
  PLAYING = 200,
  CP1W = 300,
  CP2W = 301,
}

export type playerReadyResponse = 'not user' | 'not table' | 'cannot ready' | 'not dueler' | 'ready'

export type moveResponse =
  | 'not user'
  | 'not table'
  | 'not playing'
  | 'not dueler'
  | 'not round'
  | 'P1 win'
  | 'P2 win'
  | 'done'

export async function create_table(tablepass: string): Promise<number> {
  const r = await fetch(`${API_HOST}/gomoku/table?tablepass=${tablepass}`, {
    method: 'POST',
  })
  if (r.status != 200) {
    throw ''
  }
  const v = await r.json()
  console.log(v)
  return v
}

export async function see_table(
  table_id: number,
  tablepass: string,
  uid: number,
  userpass: string,
): Promise<GomokuTableStatus> {
  const r = await fetch(`${API_HOST}/gomoku/table/${table_id}?tablepass=${tablepass}&uid=${uid}&userpass=${userpass}`)
  if (r.status != 200) throw (await r.json()).detail
  return r.json()
}

export async function enter_queue(
  table_id: number,
  tablepass: string,
  uid: number,
  userpass: string,
): Promise<boolean> {
  const r = await fetch(
    `${API_HOST}/gomoku/table/${table_id}/queue?tablepass=${tablepass}&uid=${uid}&userpass=${userpass}`,
    {
      method: 'POST',
    },
  )
  return r.json()
}

export async function player_ready(
  table_id: number,
  tablepass: string,
  uid: number,
  userpass: string,
): Promise<playerReadyResponse> {
  const r = await fetch(
    `${API_HOST}/gomoku/table/${table_id}/ready?tablepass=${tablepass}&uid=${uid}&userpass=${userpass}`,
    {
      method: 'POST',
    },
  )
  return r.json()
}

export async function do_move(
  table_id: number,
  tablepass: string,
  uid: number,
  userpass: string,
  x: number,
  y: number,
): Promise<moveResponse> {
  const r = await fetch(
    `${API_HOST}/gomoku/table/${table_id}/move?tablepass=${tablepass}&uid=${uid}&userpass=${userpass}`,
    {
      method: 'POST',
      body: JSON.stringify({ x, y }),
      headers: {
        'content-type': 'application/json',
      },
    },
  )
  return r.json()
}
