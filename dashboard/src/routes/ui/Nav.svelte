<script>
	import { onMount } from 'svelte';
	import { theme, manager } from '$lib/client';
	import { page } from '$app/stores';
	import { scale } from 'svelte/transition';
	import Icon from '@iconify/svelte';

	onMount(async () => {
		$theme = 'light';

		collapse = true;
	});

	let collapse = true;
</script>

<nav
	on:mouseenter={() => (collapse = false)}
	on:mouseleave={() => (collapse = true)}
	class="
    z-50
    duration-500
    rounded-[10px]
    fixed left-0 top-0 bottom-0 bg-backgroundSecondary flex flex-col box-content w-[24px] justify-between my-auto py-[37px] px-[33px] shadow-xl transition-all max-h-[600px]
    hover:max-h-full hover:w-[160px]
  "
>
	<!-- hover:max-h-full hover:w-[280px] -->

	<div class="w-full flex items-center gap-4">
		<div class="avatar w-[24px] h-[24px]">
			<img
				alt="avatar"
				src="https://avataaars.io/?avatarStyle=Circle&topType=LongHairStraight&accessoriesType=Blank&hairColor=BrownDark&facialHairType=Blank&clotheType=BlazerShirt&eyeType=Default&eyebrowType=Default&mouthType=Default&skinColor=Light"
			/>
		</div>
		{#if !collapse}
			<div transition:scale={{ delay: 100 }}>
				<span class="font-bold">
					{$manager?.lastName}
				</span><br />
				<span>
					{$manager?.firstName}
				</span>
			</div>
		{/if}
	</div>
	<div class="w-full flex flex-col gap-[60px]">
		<a
			class:bg-secondary={$page.url.href.endsWith('users')}
			class="rounded-xl flex items-center gap-4 transition hover:text-primary"
			href="/users"
			><Icon icon="mdi:users" width="24" />
			{#if !collapse}
				<span class="font-bold" transition:scale={{ delay: 100 }}>
					Дашборд <br />
					направления
				</span>
			{/if}
		</a>
		<a
			class:bg-secondary={$page.params.userId}
			class="rounded-xl flex items-center gap-4 transition hover:text-primary"
			href="/users/1"
			><Icon icon="mdi:user" width="24" />
			{#if !collapse}
				<span class="font-bold" transition:scale={{ delay: 100 }}>
					Дашборд <br />
					сотрудника
				</span>
			{/if}
		</a>
		<a
		class:bg-secondary={$page.url.href.endsWith('upload')}
		class="rounded-xl flex items-center gap-4 transition hover:text-primary"
			href="/upload"
			><Icon icon="material-symbols:upload" width="24" />
			{#if !collapse}
				<span class="font-bold" transition:scale={{ delay: 100 }}>
					Ручная <br />
					Выгрузка
				</span>
			{/if}
		</a>
	</div>

	<div class="w-full flex flex-col gap-[60px]">
		<button
			class="flex items-center gap-4 transition hover:text-primary"
			on:click={() => ($theme = $theme === 'light' ? 'dark' : 'light')}
		>
			{#if $theme === 'light'}
				<Icon icon="ph:sun-fill" width="24" />
			{:else}
				<Icon icon="ph:moon-fill" width="24" />
			{/if}
			{#if !collapse}
				<span class="font-bold text-left" transition:scale={{ delay: 100 }}>
					Поменять <br />
					тему
				</span>
			{/if}
		</button>

		<!-- <a class="flex items-center gap-4 w-full transition hover:text-primary" href="/users"
			><Icon icon="material-symbols:settings" width="24" />
			{#if !collapse}
				<span class="font-bold" transition:scale={{ delay: 100 }}> Настройки </span>
			{/if}
		</a> -->
		<a class="flex items-center gap-4 w-full transition text-error" href="/logout"
			><Icon icon="iconamoon:exit-fill" width="24" />

			{#if !collapse}
				<span class="font-bold" transition:scale={{ delay: 100 }}> Выйти </span>
			{/if}
		</a>
	</div>
</nav>
