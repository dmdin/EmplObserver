<script lang="ts">
	import { onMount } from 'svelte';
	import Icon from '@iconify/svelte';

	import { rpc, users, type Users } from '$lib/client';
	import { page } from '$app/stores';
	import { TimeInterval } from '$lib/enums';

	import { period } from './controller';
	import Bar from './ui/WorkActivity.svelte';
	import Donut from './ui/donut.svelte';
	import Badge from './ui/Badge.svelte';

	function getUser(userId: string, users: Users) {
		return $users.find((u) => u.userId === Number(userId));
	}
	$: user = getUser($page.params.userId, $users);
</script>

{#if user}
	<div class="w-full flex items-center justify-between">
		<div class="flex item-center justify-center text-2xl gap-7">
			<h2 class="font-black">Дашборд сотрудника</h2>
			<span class="text-content3">№{user.userId} / {user.domainName}</span>
		</div>
		<div class="flex items-center gap-2 font-bold py-1">
			<div class="flex items-center gap-2 bg-backgroundSecondary px-3 py-2 rounded-md">
				<Icon class="text-primary" icon="uis:calender" />
				<select bind:value={$period} class="bg-transparent w-[100px]">
					{#each Object.entries(TimeInterval) as [k, v]}
						<option value={v}>
							{v}
						</option>
					{/each}
				</select>
			</div>
		</div>
	</div>
	<div class="flex justify-between w-full my-8">
		<Badge title="Проработанные часы" value="20" measure="часов" icon="mdi:clock" />
		<Badge title="Популярное приложение" value="VK" measure="5 часов" icon="ph:align-top-fill"/>
		<Badge title="Средняя активность" value="2" measure="часа в день" icon="tabler:activity" label="Количество часов возросло"/>
		<Badge title="Вероятность увольнения" value="100%" measure="" icon="mdi:bell-cancel" label="Не эффективный сотрудник"/>
	</div>
	<div class="w-full flex mt-3 items-center justify-between gap-4 [608px]">
		<div class="flex flex-col w-4/6 gap-4">
			<Bar class="w-full" />
			<Bar class="w-full" />
		</div>
		<Donut class="h-[608px] w-2/6" />
	</div>
{/if}
