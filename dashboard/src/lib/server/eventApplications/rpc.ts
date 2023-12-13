import {rpc} from '@chord-ts/rpc'
import {db} from '../db' 
import {eventApplications} from './model'
import { applications } from '../applications/model'
import { and, eq, gt, gte, lt, sql } from 'drizzle-orm'
import { users } from '../users/model'
import { numeric } from 'drizzle-orm/pg-core'
import { TimeInterval } from '$lib/enums'

export class EventApplication {
  @rpc()
  async getForUser(user_id: number, timeInterval: TimeInterval) {

    const startDate: Date = this.getStartDateInterval(timeInterval);

    const rows = await db.select({
        app: applications.appName,
        count: sql<number>`cast(sum(count) as int)`,
      }).from(eventApplications)
        .leftJoin(applications, eq(applications.id, eventApplications.application))
        .leftJoin(users, eq(users.id, eventApplications.user))
        .where(and(eq(eventApplications.user, user_id), gt(eventApplications.date, String(startDate))))
        .groupBy(applications.id)

    const apps = rows.map(x => x.app);
    const appCounts = rows.map(x => x.count);

    return {apps: apps, appCounts: appCounts}
    
  }

  getStartDateInterval(timeInterval: TimeInterval): Date {
    let daysToSubtract: number = 0
    switch (timeInterval) {
        case TimeInterval.Day:
          daysToSubtract = 1;
          break;
        case TimeInterval.Week:
          daysToSubtract = 7;
            break;
        case TimeInterval.Month:
          daysToSubtract = 30;
            break;
        case TimeInterval.Year:
          daysToSubtract = 365;
            break;
    }

    const date = new Date();

    date.setDate(date.getDate() - daysToSubtract);
    return date;
  }
}