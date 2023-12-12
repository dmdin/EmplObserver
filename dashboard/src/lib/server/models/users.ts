import { varchar, serial, pgTable } from "drizzle-orm/pg-core";

export const users = pgTable('user', {
  id: serial('id').primaryKey(),
  domainName: varchar('domainName', { length: 100 }),
});