import './lib/supabase';
import { getSupabase } from '@supabase/auth-helpers-sveltekit';
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  const { session, supabaseClient } = await getSupabase(event);

  event.locals.sb = supabaseClient;
  event.locals.session = session;
  event.locals.email = event.cookies.get("email")
  event.locals.getSession = async () => {
    const {
      data: { session },
    } = await event.locals.sb.auth.getSession()
    return session
  }

  return resolve(event);
};