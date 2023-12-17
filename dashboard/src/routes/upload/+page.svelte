<script lang="ts">
	import { fade } from 'svelte/transition';
	const PUBLIC_API = 'http://178.170.196.177:8000';

	let files: FileList;

	let min_date, max_date, valid, message;

	async function uploadFile(attachment: FileList) {
		if (!attachment) return;

		const form = new FormData();
		const [file] = attachment;

		console.log(file);
		form.append('file', file);

		({ valid, message, min_date, max_date } = await fetch(`${PUBLIC_API}/get_dates`, {
			body: form,
			headers: {},
			method: 'POST'
		}).then((r) => r.json()));

		console.log(valid, message, min_date, max_date);
		setTimeout(() => {
			message = '';
		}, 3000);
	}

	let date;

	$: console.log(date);

	$: uploadFile(files);
</script>

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

<div class="flex w-fit gap-7 bg-backgroundSecondary shadow-md p-4 rounded-md">
	<label class="flex flex-col gap-2"
		>CSV Выгрузка
		<input accept="text/csv" bind:files id="csv" name="csv" type="file" class="input-file" />
	</label>

	<!-- {#if min_date && max_date} -->
	<!-- <input type="date" id="start" name="trip-start" value="2018-07-22" min={min_date} max={max_date} /> -->
	<label class="flex flex-col gap-2">
		Дата прогноза
		<input
			type="date"
			id="start"
			name="trip-start"
			bind:value={date}
			min="2018-01-01"
			max="2018-12-31"
			class="input"
		/>
	</label>
</div>
<!-- {/if} -->
<div></div>
