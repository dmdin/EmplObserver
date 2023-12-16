<script lang="ts">
  import {rpc} from '$lib/client'
  import {onMount} from 'svelte'
  import {goto} from '$app/navigation'
  import Icon from '@iconify/svelte'

  type Users = Awaited<ReturnType<typeof rpc.User.getAll>>
  let users: Users = []
  onMount(async() => {
    users = await rpc.User.getAll()
  })
</script>


<div class="flex w-full overflow-x-auto m-auto max-w-2xl">
	<table class="table-hover table">
		<thead>
			<tr>
				<th>№</th>
				<th><span class="flex items-center !border-0 gap-2"><Icon icon="mdi:user" class="!border-0"/> Пользователь</span></th>
				<th><span class="flex items-center !border-0 gap-2"><Icon icon="ic:outline-email" class="!border-0"/>Email</span></th>
				<th>Amount</th>
			</tr>
		</thead>
		<tbody>
      {#each users as user, i (user.id)}
        <tr class="cursor-pointer" on:click={() => {goto(`users/${user.id}`)}}>
          <th>{i + 1}</th>
          <td>{user.domainName}</td>
          <td>{user.domainEmail}</td>
          <td>{user.password}</td>
        </tr>
      {/each}
		</tbody>
	</table>
</div>