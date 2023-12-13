import { varchar, serial, pgTable, integer, date } from "drizzle-orm/pg-core";
import { applications } from "../applications/model";
import { users } from "../users/model";

export const eventApplications = pgTable('eventapplication', {
  id: serial('id').primaryKey(),
  count: integer('count'),
  date: date('date'),
  application: integer('application_id').references(() => applications.id, {onDelete: 'cascade'}).notNull(),
  user: integer('user_id').references(() => users.id, {onDelete: 'cascade'}).notNull()
});