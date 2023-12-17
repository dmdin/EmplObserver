import {error, redirect} from '@sveltejs/kit'

export async function load({locals, cookies}) {
  const { error: err } = await locals.sb.auth.signOut();
  console.log(1)
  if (err) {
    throw error(500, 'Something went wrong logging you out.');
  }
  cookies.delete('email')
  throw redirect(303, '/');
}