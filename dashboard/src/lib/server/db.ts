import { drizzle } from 'drizzle-orm/postgres-js';
// import { migrate } from 'drizzle-orm/postgres-js/migrator';
import postgres from 'postgres';
import {DB} from '$env/static/private'

const queryClient = postgres(DB);
export const db = drizzle(queryClient);
