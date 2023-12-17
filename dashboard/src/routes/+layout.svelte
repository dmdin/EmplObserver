<script>
	import '../app.css';
	import { onMount } from 'svelte';
	import { rpc, manager, theme } from '$lib/client';
	import {page} from '$app/stores'
	import Nav from './ui/Nav.svelte'

	$: console.log($page.data)
	onMount(async () => {
		$manager = await rpc.Managers.getManagerInfo();
	});
</script>

<div id="theme-root" data-theme={$theme} class="w-full h-full min-h-[100vh] bg-backgroundPrimary">
	{#if $page.data.session}
  	<Nav/>
	{/if}
	<main class="w-full p-2 flex- flex-col max-w-5xl m-auto py-[50px] ">
		<slot />
	</main>
</div>
