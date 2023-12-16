<script lang="ts">
	import { onMount } from 'svelte';
	import dayjs from 'dayjs';
	import { Chart, type EChartsOptions } from 'svelte-echarts';
	import { page } from '$app/stores';
	import { rpc, colors } from '$lib/client';
	import type { TimeInterval } from '$lib/enums';
	import { period } from '../controller';

	const userId = Number($page.params.userId);

	let loading = true;

	async function update(period: TimeInterval, $colors) {
		loading = true;
		const events = await rpc.EventTimeInterval.getForUser(userId, period);

		const time = [];
		const values = [];

		for (const event of events) {
			// dayjs(event.intervalEnd).fo)
			time.push(dayjs(event.intervalEnd).format('HH:mm'));
			values.push(event.count);
		}

		loading = false;
		return {
			title: {
				textStyle: {
					color: $colors?.c1
				},
				text: 'Распределение активности'
			},
			label: {
				color: $colors?.c1
			},

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
			grid: {
				left: '10%',
				right: '5%',
				bottom: '10%',
				top: '20%'
				// borderColor: hsl2css(vars?.b2),
			},
			series: [
				{
					data: values,
					type: 'bar'
				}
			]
		};
	}

	$: options = update($period, $colors);
</script>

<div class="p-3 w-fit bg-backgroundSecondary rounded-md {$$props.class}">
	<div class="min-h-[272px] h-full w-full grid place-items-center">
		{#await options}
			<div class="spinner-circle"></div>
		{:then options}
			<Chart {options} />
		{/await}
	</div>
</div>
