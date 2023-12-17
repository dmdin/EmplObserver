<script lang="ts">
	import { fade } from 'svelte/transition';
	import Icon from '@iconify/svelte';

	import Badge from '$lib/ui/Badge.svelte';
	import Percent from '$lib/ui/Percent.svelte';
	import { round } from '$lib/client';

	const PUBLIC_API = 'http://178.170.196.177:8000';

	let files: FileList;

	let min_date, max_date, valid, message, stats;

	let result = 0;

	async function uploadFile(attachment: FileList) {
		if (!attachment) return;

		const form = new FormData();
		const [file] = attachment;

		form.append('file', file);

		({ valid, message, min_date, max_date, stats } = await fetch(`${PUBLIC_API}/get_dates`, {
			body: form,
			headers: {},
			method: 'POST'
		}).then((r) => r.json()));

		console.log(valid, message, min_date, max_date);
		setTimeout(() => {
			message = '';
		}, 3000);
	}

	async function getData(date) {
		const attachment = files;
		if (!attachment || !date) return;

		const form = new FormData();
		const [file] = attachment;

		form.append('file', file);
		form.append('date_diff', date);

		({ valid, message, result } = await fetch(`${PUBLIC_API}/upload`, {
			body: form,
			headers: {},
			method: 'POST'
		}).then((r) => r.json()));

		console.log(valid, message, result);
		setTimeout(() => {
			message = '';
		}, 3000);
	}

	let date;

	$: uploadFile(files);
	$: getData(date);
</script>

<div class="w-full flex items-center justify-between mb-5">
	<div class="flex item-center justify-center text-2xl gap-7">
		<h2 class="font-black whitespace-nowrap">Дашборд c ручной выгрузкой</h2>

		<!-- <span class="text-sm flex items-center text-content3 truncate"
      >{$manager?.departmentName}</span
    > -->
	</div>
	<div class="flex w-fit gap-7 bg-backgroundSecondary shadow-md px-2 py-1 rounded-md">
		<span> Выберите файл со статистикой и дату для разбиения на два временных интервала </span>
		<label class="flex gap-2 items-center justify-center">
			<Icon class="text-primary" icon="mdi:file-outline" width="24" />
			<input accept="text/csv" bind:files id="csv" name="csv" type="file" class="input-file" />
		</label>

		<!-- {#if min_date && max_date} -->
		<!-- <input type="date" id="start" name="trip-start" value="2018-07-22" min={min_date} max={max_date} /> -->
		<label class="flex gap-2 justify-between items-center">
			<Icon class="text-primary" icon="mdi:calendar" width="24" />
			{#key min_date && max_date}
				<input
					type="date"
					id="start"
					name="trip-start"
					disabled={!(min_date && max_date)}
					bind:value={date}
					min={min_date}
					max={max_date}
					class="input"
				/>
			{/key}
		</label>
	</div>
</div>

{#if message}
	<div class="w-full px-6 top-5 left-0 absolute">
		<div class="alert alert-error w-full px-2" transition:fade>
			<svg
				width="48"
				height="48"
				viewBox="0 0 48 48"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					fill-rule="evenodd"
					clip-rule="evenodd"
					d="M24 4C12.96 4 4 12.96 4 24C4 35.04 12.96 44 24 44C35.04 44 44 35.04 44 24C44 12.96 35.04 4 24 4ZM24 26C22.9 26 22 25.1 22 24V16C22 14.9 22.9 14 24 14C25.1 14 26 14.9 26 16V24C26 25.1 25.1 26 24 26ZM26 34H22V30H26V34Z"
					fill="#E92C2C"
				/>
			</svg>
			<div class="flex flex-col w-11/12">
				<span class="text-content2 truncate">{message}</span>
			</div>
		</div>
	</div>
{/if}

<!-- {/if} -->
<div class="w-full flex justify-between items-center">
	<Badge />
	<Badge />
	<Badge />
	<Badge />
</div>

<div class="w-1/2 mt-5 flex justify-between p-4 bg-backgroundSecondary shadow-md">
	<h1 class="font-bold text-3xl">Вероятность увольнения:</h1>
	<Percent class="text-7xl font-black" value={result} />
</div>
