import { varchar, serial, pgTable } from "drizzle-orm/pg-core";

export const applications = pgTable('app', {
  id: serial('id').primaryKey(),
  appName: varchar('appName', { length: 100 }),
});