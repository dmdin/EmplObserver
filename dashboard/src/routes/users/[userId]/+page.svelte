<script lang="ts">
	import { rpc, users, type Users } from '$lib/client';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { TimeInterval } from '$lib/enums';
	import { period } from './controller';
	import Bar from './ui/WorkActivity.svelte';
	import Donut from './ui/donut.svelte';

	function getUser(userId: string, users: Users) {
		return $users.find((u) => u.userId === Number(userId));
	}
	$: user = getUser($page.params.userId, $users);
</script>

{#if user}
	<div class="w-full flex items-center justify-between mb-10 mt-[50px]">
		<div class="flex item-center justify-center text-2xl gap-7">
			<h2 class="font-black">Дашборд сотрудника</h2>
			<span class="text-content3">№{user.userId} / {user.domainName}</span>
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
	<div class="w-full flex mt-3 items-center justify-between gap-4 [608px]">		<div class="flex flex-col w-4/6 gap-4">
			<Bar class="w-full" />
			<Bar class="w-full" />
		</div>
		<Donut class="h-[608px] w-2/6" />
	</div>
{/if}
