<script lang="ts">
	import { onMount } from 'svelte';
	import dayjs from 'dayjs';
	import { Chart, type EChartsOptions } from 'svelte-echarts';
	import { page } from '$app/stores';
	import { rpc, colors,  } from '$lib/client';
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
			time.push(dayjs(event.intervalEnd).format('HH:mm-DD/MM'));
			values.push({
				value: event.count,
				itemStyle: {
					borderRadius: [20, 20, 20, 20],
					color: $colors.p // Change the color here
				}
			});
		}

		loading = false;
		return {
			// color: [$colors?.p],

			title: {
				text: 'Распределение активности',
				textStyle:{
					color: $colors?.c1
				}
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
				left: '12%',
				right: '5%',
				bottom: '10%',
				top: '20%'

				// borderColor: hsl2css(vars?.b2),
			},

			series: [
				{
					data: values,
					type: 'bar',
					showBackground: true,
					backgroundStyle: {
						borderRadius: [20, 20, 20, 20],
						color: $colors.s
					}
				}
			]
		};
	}

	$: options = update($period, $colors);
</script>

<div class="p-3 w-fit bg-backgroundSecondary rounded-md {$$props.class} shadow-md">
	<div class="min-h-[272px] h-full w-full grid place-items-center">
		{#await options}
			<div class="spinner-circle"></div>
		{:then options}
			<Chart {options} />
		{/await}
	</div>
</div>
