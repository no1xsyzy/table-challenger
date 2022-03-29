<script lang="ts">
  import { goto } from '$app/navigation'

  import { localStore } from '$lib/store'
  import * as user from '$lib/user'
  import { get } from 'svelte/store'

  const user_id = localStore('user_id', 0)
  const userpass = localStore('userpass', '')
  let user_name: string
  let message = ''

  $: get(localStore('user_id', 0)) != 0 && goto(`/user/${$user_id}`)

  $: user.user_info($user_id).then(
    (s) => (user_name = s.user_name),
    (e) => console.log(e),
  )

  const login = async () => {
    try {
      const u = await user.login($user_id, $userpass)
      message = 'success!'
    } catch (err) {
      message = err
    }
  }

  const register = async () => {
    const pass = prompt('user password?')
    if (pass == null) return
    let id = await user.register(pass)
    $user_id = id
    $userpass = pass
    goto(`/user/${id}`)
  }
</script>

<h1><a href="/">Home</a> / User</h1>

<div>
  <input type="text" bind:value={$user_id} />
</div>
<div>
  <input type="password" bind:value={$userpass} />
</div>
<div>
  <button on:click={login}>Login</button>
  <button on:click={register}>Register</button>
</div>
<div>{message}</div>
