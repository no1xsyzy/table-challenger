import { API_HOST } from './API_HOST'
import type { User } from '$lib/types/user'

export async function register(userpass: string): Promise<number> {
  const r = await fetch(`${API_HOST}/users?userpass=${userpass}`, { method: 'POST' })
  return r.json()
}

export async function login(uid: number, userpass: string): Promise<User> {
  const r = await fetch(`${API_HOST}/users/login?uid=${uid}&userpass=${userpass}`, { method: 'POST' })
  if (r.status == 200) return r.json()
  else throw (await r.json()).detail
}

export async function user_info(uid: number): Promise<User> {
  const r = await fetch(`${API_HOST}/users/${uid}`)
  if (r.status == 200) return r.json()
  else throw (await r.json()).detail
}

export async function rename(uid: number, userpass: string, name: string): Promise<number> {
  const r = await fetch(`${API_HOST}/users/${uid}/name?userpass=${userpass}&name=${name}`, { method: 'PUT' })
  return r.json()
}
