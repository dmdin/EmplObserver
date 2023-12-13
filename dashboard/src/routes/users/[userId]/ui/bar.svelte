<script lang="ts">
	import { onMount } from 'svelte';
	import dayjs from 'dayjs';
	import { Chart, type EChartsOptions } from 'svelte-echarts';

	import { page } from '$app/stores';
	import { rpc } from '$lib/client';
	import type { TimeInterval } from '$lib/enums';
	import { period } from '../controller';

	const userId = Number($page.params.userId);

	let loading = true;

	async function update(period: TimeInterval) {
		loading = true;
		const events = await rpc.EventTimeInterval.getForUser(userId, period);
		console.log(events);

		const time = [];
		const values = [];

		for (const event of events) {
			// dayjs(event.intervalEnd).fo)
			time.push(dayjs(event.intervalEnd).format('HH:mm'));
			values.push(event.count);
		}

		console.log(events);
		loading = false;
		return {
			tooltip: {
				confine: true,
				textStyle: {
					fontFamily: 'SBSans',
					fontWeight: 'normal',
					fontSize: 12
				},
				trigger: 'axis',
				axisPointer: {
					type: 'cross'
				}
			},
			toolbox: {
				feature: {
					saveAsImage: {}
				}
			},
			xAxis: {
				data: time,
				type: 'category'
			},
			yAxis: {
				type: 'value'
			},
			series: [
				{
					data: values,
					type: 'bar',
				}
			]
		};
	}

	$: options = update($period);
</script>

<div class="w-[400px] h-[300px]">
	{#await options}
		<div class="spinner-circle"></div>
	{:then options}
		<Chart {options} />
	{/await}
</div>
