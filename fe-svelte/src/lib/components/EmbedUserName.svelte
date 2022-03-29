<script lang="ts">
  import { localStore } from '$lib/store'
  import * as user from '$lib/user'

  const user_id = localStore('user_id', 0)
  const userpass = localStore('userpass', '')
  let user_name: string

  $: user.user_info($user_id).then(
    (s) => (user_name = s.user_name),
    (e) => console.log(e),
  )
</script>

{#if $user_id}
  <span class="username"
    >Hello, {user_name} (<a
      href="#:"
      on:click={(e) => {
        e.preventDefault()
        const new_name = prompt('new name?')
        if (new_name == null) return
        user_name = new_name
        user.rename($user_id, $userpass, new_name)
      }}>Rename</a
    >)</span
  >
{:else}
  <span class="username"
    >Guest, you can <a
      href="#:"
      on:click={(e) => {
        e.preventDefault()
        const pass = prompt('user password?')
        if (pass == null) return
        user.register(pass).then((id) => {
          $user_id = id
          $userpass = pass
        })
      }}>register</a
    >!</span
  >
{/if}
