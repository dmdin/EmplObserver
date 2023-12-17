import { varchar, serial, pgTable, integer, time } from "drizzle-orm/pg-core";

export const users = pgTable('user', {
  id: serial('id').primaryKey(),
  domainName: varchar('domainName', { length: 100 }),
  domainEmail: varchar('domainEmail', { length: 100 }),
  password: varchar('password', { length: 100 }),
  managerId: integer('managerid')
});

export class updateUserModel{
  id: number | undefined
  domainName: string | undefined
  domainEmail: string | undefined
  password: string | undefined
}

export class userUpdateMessage{
  userId: number | undefined
  success: boolean | undefined
  message: string | undefined
}

export const timeIntervalEvents = pgTable('timeintervalevent', {
  id: serial('id').primaryKey(),
  count: integer('count'),
  intervalStart: time('intervalStart'),
  intervalEnd: time('intervalEnd'),
  user: integer('user_id').references(() => users.id, {onDelete: 'cascade'}).notNull()
});