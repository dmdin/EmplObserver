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
		const {apps, appCounts} = await rpc.EventApplication.getForUser(userId, period);
		console.log(apps);


		console.log(apps);
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

			series: [
				{
					data: apps.map((a, i) => { return {
            name: a,
            value: appCounts[i]
          }}),
					type: 'pie',
          radius: ['65%', '70%'],
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
