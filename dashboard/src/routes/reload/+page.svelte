<script>
	import { page } from '$app/stores';
	import { goto, invalidateAll } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(async () => {
		await invalidateAll();
		if ($page.data.session) {
			await goto('/users');
		} else {
			await goto('/');
		}
	});
</script>
