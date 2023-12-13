import {rpc} from '@chord-ts/rpc'
import {db} from '../db' 
import {timeIntervalEvents} from './model'
import { and, eq, gt} from 'drizzle-orm'
import type { TimeInterval } from '../models/TimeInverval'

export class EventTimeInterval {
  @rpc()
  async getForUser(user_id: number, timeInterval: TimeInterval) {

    let startDate: Date = this.getStartDateInterval(timeInterval);

    return await db.select()
        .from(timeIntervalEvents)
        .where(and(eq(timeIntervalEvents.user, user_id), gt(timeIntervalEvents.intervalStart, String(startDate))))
    
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