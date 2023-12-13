import { AuthApiError, type Provider } from '@supabase/supabase-js';
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

const OAUTH_PROVIDERS = ['google'];

export const actions: Actions = {
  login: async ({ request, locals, url, cookies }) => {
    const provider = url.searchParams.get('provider') as Provider;

    if (provider) {
      if (!OAUTH_PROVIDERS.includes(provider)) {
        return fail(400, {
          error: 'Provider not supported.'
        });
      }
      const { data, error: err } = await locals.sb.auth.signInWithOAuth({
        provider: provider
      });

      if (err) {
        console.error(err);
        return fail(400, {
          message: 'Something went wrong.'
        });
      }

      throw redirect(303, data.url);
    }

    const body = Object.fromEntries(await request.formData());

    const {email, password} = body

    if (email === 'bobip@yandex.ru' && password === 'qwerty') {
      cookies.set('email', email)
      throw redirect(303, '/taskAssigns')
    }
    // const { data, error: err } = await locals.sb.auth.signInWithPassword({
    //   email: body.email as string,
    //   password: body.password as string
    // });
    console.log(email, passw)
    if (err) {
      if (err instanceof AuthApiError && err.status === 400) {
        return fail(400, {
          error: 'Invalid credentials'
        });
      }
      return fail(500, {
        message: 'Server error. Try again later.'
      });
    }

    throw redirect(303, '/');
  }
};

export async function load({locals}) {
  if (locals?.session) throw redirect(303, '/tasks')
}