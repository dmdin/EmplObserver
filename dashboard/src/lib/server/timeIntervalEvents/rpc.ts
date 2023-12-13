import {rpc} from '@chord-ts/rpc'
import {db} from '../db' 
import {timeIntervalEvents} from './model'
import { and, eq, gt} from 'drizzle-orm'
import { TimeInterval } from '$lib/enums'

export class EventTimeInterval {
  @rpc()
  async getForUser(user_id: number, timeInterval: TimeInterval) {

    const startDate: Date = this.getStartDateInterval(timeInterval);

    return await db.select()
        .from(timeIntervalEvents)
        .where(and(eq(timeIntervalEvents.user, user_id), gt(timeIntervalEvents.intervalStart, String(startDate))))
    
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