import {supabaseClient} from '$lib/supabase'


export const load = async ({ fetch, data, depends }) => {
  // depends('supabase:auth')

  const {
    data: { session },
  } = await supabaseClient.auth.getSession()

  return { supabase: supabaseClient, session }
}