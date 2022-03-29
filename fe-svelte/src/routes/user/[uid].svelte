<script lang="ts">
  import { getStores } from '$app/stores'

  import { localStore } from '$lib/store'
  import * as user from '$lib/user'

  const { page } = getStores()

  export let uid = +$page.params.uid
  const user_id = localStore('user_id', 0)
  const userpass = localStore('userpass', '')
  let user_name: string
  let shading = true

  $: itsme = uid == $user_id

  $: user.user_info(uid).then(
    (s) => (user_name = s.user_name),
    (e) => console.log(e),
  )
</script>

<svelte:head>
  <title>User</title>
</svelte:head>

<h1><a href="/">Home</a> / User</h1>

{#if uid}
  <table>
    <tbody>
      <tr>
        <td>user_id</td>
        <td>{uid}</td>
      </tr>
      <tr>
        <td>user_name</td>
        {#if user_name}
          <td>{user_name}</td>
        {:else}
          <td class="fetching">fetching...</td>
        {/if}
      </tr>
      {#if itsme}
        <tr>
          <td>userpass</td>
          <td>
            {#if shading}
              <span on:click={() => (shading = false)}>***</span>
            {:else}
              <span on:click={() => (shading = true)}>{$userpass}</span>
            {/if}
          </td>
        </tr>
      {/if}
    </tbody>
  </table>
{/if}

<style>
  .fetching {
    color: grey;
  }
</style>
