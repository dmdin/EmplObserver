<script lang="ts">
  import {rpc} from '$lib/client'
  import {onMount} from 'svelte'
  
  import {TimeInterval} from '$lib/enums'
  import {period} from './controller'
  import Bar from './ui/bar.svelte'
  import Donut from './ui/donut.svelte';

</script>

<select bind:value={$period} class="select">
  {#each Object.entries(TimeInterval) as [k, v]}
    <option value={v}>
      {v}
    </option>
  {/each}
</select>
<Donut/>
<Bar/>
