<script lang="ts">
	import { manager, rpc } from '$lib/client';
	import { TimeInterval } from '$lib/enums';
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { goto } from '$app/navigation';
	import Icon from '@iconify/svelte';

	type Users = Awaited<ReturnType<typeof rpc.User.getAll>>;
	let users: Users = [];
	onMount(async () => {
		users = await rpc.User.getAll();
    console.log(users)
	});

	const period = writable();
</script>

<div class="w-full overflow-x-auto m-auto flex flex-col">
	<div class="w-full flex items-center justify-between mb-5">
		<div class="flex item-center justify-center text-2xl gap-7">
			<h2 class="font-black whitespace-nowrap">Дашборд направления</h2>
			<span class="text-sm flex items-center text-content3 truncate"
				>{$manager?.departmentName}</span
			>
		</div>
		<div class="flex items-center gap-2 font-bold bg-content3/10 px-4 py-1 rounded">
			<h3>Выбор периода:</h3>
			<select bind:value={$period} class="select w-[100px]">
				{#each Object.entries(TimeInterval) as [k, v]}
					<option value={v}>
						{v}
					</option>
				{/each}
			</select>
		</div>
	</div>

	<div class="bg-backgroundSecondary p-3 border border-border rounded-md">
		<table class="table-hover table">
			<thead>
				<tr>
					<th>№</th>
					<th
						><span class="flex items-center !border-0 gap-2"
							><Icon icon="mdi:user" class="!border-0" /> Пользователь</span
						></th
					>
					<th
						><span class="flex items-center !border-0 gap-2"
							><Icon icon="ic:outline-email" class="!border-0" />Email</span
						></th
					>
					<th>Amount</th>
				</tr>
			</thead>
			<tbody>
				{#each users as user, i (user.userId)}
					<tr
						class="cursor-pointer"
						on:click={() => {
							goto(`users/${user.userId}`);
						}}
					>
						<th>{i + 1}</th>
						<td>{user.domainName}</td>
						<td>{user.domainEmail}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
