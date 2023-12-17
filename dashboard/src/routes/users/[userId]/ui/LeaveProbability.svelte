<script lang="ts">
	import { onMount } from 'svelte';
	import dayjs from 'dayjs';
	import { Chart, type EChartsOptions } from 'svelte-echarts';
	import { page } from '$app/stores';
	import { rpc, colors,  } from '$lib/client';
	import type { TimeInterval } from '$lib/enums';
	import { period } from '../controller';
	import { number } from 'echarts';

	const userId = Number($page.params.userId);

	let loading = true;

	async function update(period: TimeInterval, $colors) {
		loading = true;
		const events = (await rpc.User.getForUserByDiap(userId, period));
		console.log(events)

		const time = [];
		const values = [];
		const millisecondsInDay = 24 * 60 * 60 * 1000;
		var start_date = dayjs();
		start_date = start_date.subtract(Math.max(events.length-1, 0), 'day');
		
		var i = 0;

		for (const event of events) {
			time.push(JSON.stringify(start_date.get('date')));
			start_date = start_date.add(1, 'day');
			values.push({
				value: event.dismissalProbability,
				itemStyle: {
					borderRadius: [20, 20, 20, 20],
					color: $colors.p, // Change the color here
				}
			});
		}
		console.log(values.length, time.length)
		loading = false;
		return {
			// color: [$colors?.p],

			title: {
				text: '	Вероятность увольнения сотрудника',
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
				type: 'value',
				max: 1
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
					},
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
