import { error, redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ locals, cookies }) => {
  const { error: err } = await locals.sb.auth.signOut();
  console.log(1)
  if (err) {
    throw error(500, 'Something went wrong logging you out.');
  }
  cookies.delete('email')
  throw redirect(303, '/');
};