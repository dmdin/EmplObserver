<script lang="ts">
	import { enhance, type SubmitFunction } from '$app/forms';
	import { supabaseClient } from '$lib/supabase';
	import type { Provider } from '@supabase/supabase-js';
	import Icon from '@iconify/svelte';

	const signInWithProvider = async (provider: Provider) => {
		const { data, error } = await supabaseClient.auth.signInWithOAuth({
			provider: provider
		});
	};

	const submitSocialLogin: SubmitFunction = async ({ action, cancel }) => {
		switch (action.searchParams.get('provider')) {
			case 'google':
				await signInWithProvider('google');
				break;
			default:
				break;
		}
		cancel();
	};
</script>

<main class="flex flex-col items-center justify-center h-full">
	<h1>Войти</h1>
	<form action="?/login" method="POST" class="auth-form">
		<label class="label" for=""> Email </label>
		<input class="input input-bordered" type="text" name="email" />

		<label class="label" for=""> Пароль </label>
		<input class="input input-bordered" type="password" name="password" />
		<button type="submit" class="btn btn-primary mt-2">Войти</button>
	</form>

	<form
		class="socials flex flex-col mt-4 gap-2 border-t-2 py-5 border-base-content/20"
		method="POST"
	>
		<button formaction="?/login&provider=google" class="btn btn-outline"
			><Icon icon="flat-color-icons:google" />Google</button
		>
	</form>
</main>

<style lang="postcss">
	.auth-form {
		display: flex;
		flex-direction: column;
		width: 100%;
		max-width: 400px;
		min-width: 400px;
		margin: 0 auto;
	}

	.socials {
		width: 100%;
		max-width: 400px;
		min-width: 400px;
	}
</style>
