<script lang="ts">
	import { onMount } from 'svelte';
	import Icon from '@iconify/svelte';

	import { rpc, users, round, type Users } from '$lib/client';
	import { page } from '$app/stores';
	import { TimeInterval } from '$lib/enums';

	import { period, events, appsInfo } from './controller';
	import type { AppsInfo, Events } from './controller';

	import Bar from './ui/WorkActivity.svelte';
	import Donut from './ui/donut.svelte';
	import Badge from './ui/Badge.svelte';
	import LeaveBar from './ui/LeaveProbability.svelte';

	function getUser(userId: string, users: Users) {
		return $users.find((u) => u.userId === Number(userId));
	}
	$: user = getUser($page.params.userId, $users);

	function calcStats(events: Events, appsInfo: AppsInfo) {
		let mostUsed = { name: 'Отсутствует', value: 0 };
		let sumHours = 0;
		let sumClicks = 0;

		if (!events) return { sumHours, mostUsed, sumClicks };
		sumHours = events.filter((v) => v.count! > 100).length / 2;
		sumClicks = events.reduce((p, c) => (p += c.count!), 0);

		if (!appsInfo) return { sumHours, mostUsed, sumClicks };
		for (const [i, v] of Object.entries(appsInfo.appCounts)) {
			if (mostUsed.value < v) {
				mostUsed = { name: appsInfo.apps[Number(i)]!, value: v };
			}
		}
		return { sumHours, mostUsed, sumClicks };
	}

	let sumHours: number, mostUsed: { name: string; value: number }, sumClicks: number;
	$: ({ sumHours, sumClicks, mostUsed } = calcStats($events, $appsInfo));

	$: console.log(user)
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
		<Badge
			title="Часы работы"
			value={sumHours}
			measure="часов"
			icon="mdi:clock"
			label="Всего: {sumClicks} кликов"
		/>
		<Badge
			title="Популярное приложение"
			value={mostUsed.name}
			class="!text-[20px]"
			measure=""
			label="{mostUsed.value} кликов в приложении"
			icon="ph:align-top-fill"
		/>
		<Badge
			title="Поздно прочитанные письма"
			value={round(user.readMessagesMoreThan4Hours, 2)}
			measure="шт."
			icon="tabler:activity"
			label="Получено писем всего: {round(user.receivedMessagesCount, 2)}"
		/>
		<Badge
			title="Отправленные письма"
			value={round(user.sendMessagesCount, 2)}
			measure="шт."
			icon="mdi:bell-cancel"
			label="Всего ответов: {round(user.repliedMessagesCount)}"
		/>
	</div>
	<div class="w-full flex mt-3 items-center justify-between gap-4 [608px]">
		<div class="flex flex-col w-5/6 gap-4">
			<Bar class="w-full" />
			<LeaveBar class="w-full" />
		</div>
		<Donut class="h-[608px] w-full" />
	</div>
{/if}
