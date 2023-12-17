<script lang="ts">
	import { round } from '$lib/client';
	export let value = 0;
</script>

<h2
	class="{$$props.class}"
	class:text-primary={0.55 > value}
	class:text-warning={0.55 < value && value < 0.75}
	class:text-error={0.75 < value}
>
	{round(100 * value, 1)}%
</h2>
