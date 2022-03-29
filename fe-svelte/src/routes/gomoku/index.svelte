<script lang="ts">
  import * as gomoku from '$lib/gomoku'
  import { safeInterval } from '$lib/safeInterval'
  import { page } from '$app/stores'
  import { goto } from '$app/navigation'
  import { onMount } from 'svelte'
  import { localStore } from '$lib/store'
  import EmbedUserName from '$lib/components/EmbedUserName.svelte'

  const range = (start: number, end: number = null, step: number = null) => {
    if (end === null) {
      end = start
      start = 0
    }
    if (step === null) {
      step = 1
    }
    const lst = []
    for (let i = start; i < end; i++) {
      lst.push(i)
    }
    return lst
  }

  const constructFace = (moves: gomoku.Move[]) => {
    let face = range(15).map(() => range(15).map(() => 0))
    let black = true
    for (let { x, y } of moves) {
      face[x][y] = black ? 1 : 2
      black = !black
    }
    return face
  }

  const user_id = localStore('user_id', 0)
  const userpass = localStore('userpass', '')

  $: table_id = +($page.url.searchParams.get('table_id') ?? NaN)
  $: tablepass = $page.url.searchParams.get('tablepass')

  let tableStatus: gomoku.TableStatus

  onMount(() => {
    return safeInterval(async () => {
      if (!isNaN(table_id)) {
        try {
          tableStatus = await gomoku.see_table(table_id, tablepass, $user_id, $userpass)
        } catch (err) {
          if (err === 'not table') goto('?')
        }
      } else {
        tableStatus = null
      }
    }, 1000)
  })

  $: face = tableStatus ? constructFace(tableStatus.moves) : null
  $: p1turn = tableStatus ? tableStatus.left_is_black === (tableStatus.moves.length % 2 == 0) : null
  $: iamp1 = tableStatus?.player1?.user_id == $user_id
  $: iamp2 = tableStatus?.player2?.user_id == $user_id
  $: my_turn = tableStatus && tableStatus.state == 200 ? (p1turn ? iamp1 : iamp2) : false

  let old_state: gomoku.TableState
  $: {
    if (tableStatus?.state != old_state) {
      old_state = tableStatus?.state
      console.log('state', tableStatus?.state)
    }
  }

  const create_table = async () => {
    const tablepass = prompt('password?')
    const table_id = await gomoku.create_table(tablepass)
    goto(`?table_id=${table_id}&tablepass=${tablepass}`)
  }

  const enter_queue = async () => {
    gomoku.enter_queue(table_id, tablepass, $user_id, $userpass)
  }

  const move = async (x: number, y: number) => {
    gomoku.do_move(table_id, tablepass, $user_id, $userpass, x, y)
  }

  const ready = async () => {
    gomoku.player_ready(table_id, tablepass, $user_id, $userpass)
  }
</script>

<svelte:head>
  <title>Gomoku</title>
</svelte:head>

<h1><a href="/">Home</a> / Gomoku</h1>
<EmbedUserName />

{#if isNaN(table_id)}
  <button on:click={create_table}>create table</button>
{/if}
{#if tableStatus}
  {#if face !== null}
    <table class="face" class:my_turn>
      <tbody>
        {#each range(15) as y (y)}
          <tr>
            {#each range(15) as x (x)}
              <td
                class:black={face[x][y] == 1}
                class:white={face[x][y] == 2}
                class:empty={face[x][y] == 0}
                on:click={() => {
                  if (my_turn && face[x][y] == 0) {
                    move(x, y)
                  }
                }}
              />
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}

  <table class="players">
    <thead>
      <tr>
        <th class="left">Left</th>
        <th class="right">Right</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        {#if tableStatus.player1 !== null}
          <td class="player_name" class:me={iamp1}>
            {tableStatus.player1.user_name}
            {#if tableStatus.state >= 300}
              {#if tableStatus.state == gomoku.TableState.CP1W}
                winner {#if iamp1}
                  <button on:click={ready}>ready?</button>
                {/if}
              {/if}
            {:else if tableStatus.state == 200}
              <img src={tableStatus.left_is_black ? '/static/gomoku-black.png' : '/static/gomoku-white.png'} alt="" />
            {:else if tableStatus.state >= 100}
              {#if tableStatus.state == gomoku.TableState.P1R}
                ready✔
              {:else if iamp1}
                <button on:click={ready}>ready?</button>
              {:else}
                ready?
              {/if}
            {/if}
          </td>
        {:else}
          <td class="pending">pending...</td>
        {/if}
        {#if tableStatus.player2 !== null}
          <td class="player_name" class:me={iamp2}>
            {#if tableStatus.state >= 300}
              {#if tableStatus.state == gomoku.TableState.CP2W}
                winner {#if iamp2}
                  <button on:click={ready}>ready?</button>
                {/if}
              {/if}
            {:else if tableStatus.state == 200}
              <img src={tableStatus.left_is_black ? '/static/gomoku-white.png' : '/static/gomoku-black.png'} alt="" />
            {:else if tableStatus.state >= 100}
              {#if tableStatus.state == gomoku.TableState.P2R}
                ready✔
              {:else if iamp2}
                <button on:click={ready}>ready?</button>
              {:else}
                ready?
              {/if}
            {/if}
            {tableStatus.player2.user_name}
          </td>
        {:else}
          <td class="pending">pending...</td>
        {/if}
      </tr>
    </tbody>
  </table>

  <table class="queue">
    <thead
      ><tr>
        <th>#</th>
        <th>Queue User</th>
      </tr></thead
    >
    <tbody>
      {#each tableStatus.queue as user, idx}
        <tr class:me={user.user_id == $user_id}><td>{idx + 1}</td><td>{user.user_name}</td></tr>
      {/each}
      {#if ((x) => tableStatus.queue.filter((user) => user.user_id == x))($user_id).length == 0}
        <tr><td /><td><button on:click={enter_queue}>Queue me in</button></td></tr>
      {/if}
    </tbody>
  </table>
{/if}

<style>
  .face {
    border: 1px red;
    padding: 0;
    margin: 0;
    border-collapse: collapse;
    border: 0;
    background-image: url('/static/gomoku-board.png');
  }
  .face tr {
    height: 35px;
    padding: 0;
    margin: 0;
    border: 0;
  }
  .face td {
    width: 35px;
    text-align: center;
    padding: 0;
    margin: 0;
    border: 0;
  }
  .face td.black {
    background-image: url('/static/gomoku-black.png');
  }
  .face td.white {
    background-image: url('/static/gomoku-white.png');
  }
  .face.my_turn td.empty {
    cursor: pointer;
  }

  .players {
    width: 535px;
    border: 2px solid;
    border-collapse: collapse;
  }
  .players th,
  .players td {
    text-align: center;
    border: 1px solid;
  }
  .players td.pending {
    color: grey;
  }
  .players .me {
    background-color: beige;
  }

  .players .player_name {
    line-height: 35px;
    height: 35px;
    font-size: 35px;
  }

  .players .player_name button {
    font-size: 35px;
  }

  .queue {
    width: 535px;
  }
  .queue .me {
    background-color: beige;
  }
</style>
