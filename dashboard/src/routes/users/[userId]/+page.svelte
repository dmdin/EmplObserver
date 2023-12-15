<script lang="ts">
	import { rpc, users, type Users } from '$lib/client';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { TimeInterval } from '$lib/enums';
	import { period } from './controller';
	import Bar from './ui/bar.svelte';
	import Donut from './ui/donut.svelte';

	function getUser(userId: string, users: Users) {
		console.log(userId, users);
		return $users.find((u) => u.id === Number(userId));
	}
	$: user = getUser($page.params.userId, $users);
</script>

<div class="w-full flex items-center justify-between mb-10">
	<h2 class="font-black text-2xl">Сотрудник: {user?.domainName}</h2>
	<div class="flex items-center gap-2 font-bold">
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
<div class="w-full flex mt-3 items-center justify-between">
	<Donut />
	<Bar />
</div>
