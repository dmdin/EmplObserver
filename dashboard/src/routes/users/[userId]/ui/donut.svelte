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
  const { apps, appCounts } = await rpc.EventApplication.getForUser(userId, period);
  const sortedData = apps.map((a, i) => {
    return {
      name: a,
      value: appCounts[i]
    };
  }).sort((a, b) => b.value - a.value);
  const appCountsSum = appCounts.reduce((sum, current) => sum + current, 0);
  const sortedApps = sortedData.map(item => item.name);

  loading = false;
  return {
    title: {
      textStyle: {
        color: $colors?.c1
      },
      text: 'Используемые приложения'
    },
    tooltip: {
      confine: true,
      textStyle: {
        fontFamily: 'SBSans',
        fontWeight: 'normal',
        fontSize: 12
      },
      trigger: 'item',
	  formatter: function(params) { 
		return " " + params.value + " (" + ((params.value / appCountsSum)*100).toFixed(2) + "%)";  
	} 
    },
    toolbox: {
      feature: {
        saveAsImage: {}
      }
    },
    legend: {
      type: 'scroll',
      orient: 'horizontal',
      bottom: 10,
      left: 'center',
      data: sortedApps,
    },
    series: [
      {
        name: 'Используемые приложения', // Используется в tooltip
        data: sortedData,
        label: {
          color: $colors?.c1
        },
        type: 'pie',
        radius: ['50%', '60%'],
      }
    ]
  };
}

	$: options = update($period, $colors);
</script>

<div class="p-3 bg-backgroundSecondary rounded-md {$$props.class}">
	<div class="min-h-[272px] h-full w-full grid place-items-center">
		{#await options}
			<div class="spinner-circle"></div>
		{:then options}
			<Chart {options} />
		{/await}
	</div>
</div>
