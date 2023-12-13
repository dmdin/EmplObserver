import {  serial, pgTable, integer, time } from "drizzle-orm/pg-core";
import { users } from "../users/model";

export const timeIntervalEvents = pgTable('timeintervalevent', {
  id: serial('id').primaryKey(),
  count: integer('count'),
  intervalStart: time('intervalStart'),
  intervalEnd: time('intervalEnd'),
  user: integer('user_id').references(() => users.id, {onDelete: 'cascade'}).notNull()
});