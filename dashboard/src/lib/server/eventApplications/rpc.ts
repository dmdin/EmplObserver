import {rpc} from '@chord-ts/rpc'
import {db} from '../db' 
import {eventApplications} from './model'
import { applications } from '../applications/model'
import { and, eq, gt, gte, lt, sql } from 'drizzle-orm'
import { users } from '../users/model'
import { numeric } from 'drizzle-orm/pg-core'
import type { TimeInterval } from '../models/TimeInverval'

export class EventApplication {
  @rpc()
  async getForUser(user_id: number, timeInterval: TimeInterval) {

    let startDate: Date = this.getStartDateInterval(timeInterval);

    let rows = await db.select({
        app: applications.appName,
        count: sql<number>`cast(sum(count) as int)`,
      }).from(eventApplications)
        .leftJoin(applications, eq(applications.id, eventApplications.application))
        .leftJoin(users, eq(users.id, eventApplications.user))
        .where(and(eq(eventApplications.user, user_id), gt(eventApplications.date, String(startDate))))
        .groupBy(applications.id)

    let apps = rows.map(x => x.app);
    let appCounts = rows.map(x => x.count);

    return {apps: apps, appCounts: appCounts}
    
  }

  getStartDateInterval(timeInterval: TimeInterval): Date {
    let daysToSubtract: number = 0
    switch (timeInterval) {
        case 0:
          daysToSubtract = 1;
          break;
        case 1:
          daysToSubtract = 7;
            break;
        case 2:
          daysToSubtract = 30;
            break;
        case 3:
          daysToSubtract = 365;
            break;
    }

    const date = new Date();

    date.setDate(date.getDate() - daysToSubtract);
    return date;
  }
}