import { API_HOST } from './API_HOST'
import type { Move, GomokuTableStatus } from './types/gomoku'
export type { Move, GomokuTableStatus }

export enum TableState {
  IDLE = 'IDLE',
  P1S = 'P1S',
  P2S = 'P2S',
  BS = 'BS',
  BS_P1R = 'BS_P1R',
  BS_P2R = 'BS_P2R',
  PLAYING = 'PLAYING',
  C_P1W = 'C_P1W',
  C_P2W = 'C_P2W',
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
