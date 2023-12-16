<script>
	import '../app.css';
	import { onMount } from 'svelte';
	import { rpc, manager, theme } from '$lib/client';

	import Nav from './ui/Nav.svelte'

	onMount(async () => {
		$manager = await rpc.Managers.getManagerInfo();
	});
</script>

<div id="theme-root" data-theme={$theme} class="w-full h-screen">
  <Nav/>
	<main class="w-full p-2 flex- flex-col max-w-5xl m-auto pt-[50px]">
		<slot />
	</main>
</div>
