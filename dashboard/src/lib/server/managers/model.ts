import { varchar, serial, pgTable, integer } from "drizzle-orm/pg-core";

export const managers = pgTable('manager', {
  id: serial('id').primaryKey(),
  domainEmail: varchar('domainemail', {length: 100}),
  departmentName: varchar('departmentname', { length: 100 }),
  firstName: varchar('firstname', { length: 100 }),
  lastName: varchar('lastname', { length: 100 }),
  middleName: varchar('middlename', { length: 100 }),
});
