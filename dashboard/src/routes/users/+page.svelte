<script lang="ts">
	import { manager, rpc, round } from '$lib/client';
	import { TimeInterval } from '$lib/enums';
	import Percent from '$lib/ui/Percent.svelte';

	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { goto } from '$app/navigation';
	import Icon from '@iconify/svelte';

	type Users = Awaited<ReturnType<typeof rpc.User.getAll>>;
	let users: Users = [];
	onMount(async () => {
		users = await rpc.User.getAll();
		console.log(users);
	});

	const period = writable();
</script>

<div class="w-full overflow-x-auto m-auto flex flex-col">
	<div class="w-full flex items-center justify-between mb-5">
		<div class="flex item-center justify-center text-2xl gap-7">
			<h2 class="font-black whitespace-nowrap">Дашборд направления</h2>
			<span class="text-xl flex items-center text-content3 truncate"
				>{$manager?.departmentName}</span
			>
		</div>
	</div>

	<div class="overflow-auto bg-backgroundSecondary p-3 border border-border rounded-md">
		<table class="table-hover table ">
			<thead>
				<tr>
					<th>№</th>
					<th>
						<span class="flex items-center !border-0 gap-2">
							<Icon icon="material-symbols:percent" class="!border-0" />Вероятность <br> увольнения
						</span>
					</th>
					<th
						><span class="flex items-center !border-0 gap-2"
							><Icon icon="mdi:user" class="!border-0" /> Пользователь</span
						></th
					>
					<th
						><span class="flex items-center !border-0 gap-2"
							><Icon icon="ic:outline-email" class="!border-0" />Email</span
						>
					</th>

					<th>Отправленные<br>письма</th>
					<th>Полученные<br>письма</th>
					<th>Уникальные<br>получатели</th>
					<th>Адресаты<br>(копия)</th>
					<th>Адресаты<br>(скрытая копия)</th>
					<th>Число дней<br>(прочтение)</th>

					<th>Письма вне<br>раб. время</th>
					<th>Поздно прч.<br>письма</th>
					<th>% полученных<br>к отправленным</th>
					<th>Ответы</th>
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
						<td><Percent value={user.dismissalProbability} /></td>
						<td>{user.domainName || '-'}</td>
						<td>{user.domainEmail || '-'}</td>
						<td>{round(user.sendMessagesCount)}</td>
						<td>{round(user.receivedMessagesCount)}</td>
						<td>{round(user.recipientCounts)}</td>
						<td>{round(user.bccCount)}</td>
						<td>{round(user.ccCount)}</td>
						<td>{round(user.daysBetweenReceivedAndRead)}</td>
						<td>{round(user.messagesOutsideWorkingHours)}</td>
						<td>{round(user.readMessagesMoreThan4Hours)}</td>
						<td><Percent value={user.receivedToSentRatio} /></td>
						<td>{round(user.repliedMessagesCount)}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
