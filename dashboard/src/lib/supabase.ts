import { SUPABASE_ANON_KEY, SUPABASE_URL } from '$env/static/private';
import { createClient } from '@supabase/auth-helpers-sveltekit';

export const supabaseClient = createClient(
  'https://auhyksbbcemytznbjejy.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1aHlrc2JiY2VteXR6bmJqZWp5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTkxODYzMDQsImV4cCI6MjAxNDc2MjMwNH0.nb5B3Sibio1vIGxjy57wK8iuoaeZEr1-CVc1DNtKYYQ'
);