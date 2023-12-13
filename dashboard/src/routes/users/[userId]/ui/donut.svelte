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

		loading = false;
		return {
			title: {
				textStyle: {
					color: '#ffffff',
				},
        text: 'Используемые приложения',
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
      grid: {
      left: '10%',
      right: '5%',
      bottom: '10%',
      top: '30%',
      // borderColor: hsl2css(vars?.b2),
    },
			series: [
				{
					data: apps.map((a, i) => { return {
            name: a,
            value: appCounts[i]
          }}),
					label: {
						color: '#ffffff',

					},
					type: 'pie',
          radius: ['50%', '60%'],
				}
			]
		};
	}

	$: options = update($period);
</script>

<div class="p-3 w-fit bg-backgroundSecondary rounded-md">
<div class="w-[400px] h-[300px] grid place-items-center">
	{#await options}
		<div class="spinner-circle"></div>
	{:then options}
		<Chart {options} />
	{/await}
</div>
</div>
