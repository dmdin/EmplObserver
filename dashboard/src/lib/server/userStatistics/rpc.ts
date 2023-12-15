import {rpc} from '@chord-ts/rpc'
import {db} from '../db' 
import {userStatistic} from './model'
import { and, eq, gt} from 'drizzle-orm'
import { TimeInterval } from '$lib/enums'

export class UserStatistics {
  @rpc()
  async getForUser(user_id: number, timeInterval: TimeInterval) {

    const startDate: Date = this.getStartDateInterval(timeInterval);

    return await db.select()
        .from(userStatistic)
        .where(and(eq(userStatistic.user, user_id), gt(userStatistic.startInterval, String(startDate))))
        .orderBy(userStatistic.startInterval)
    
  }

  async getCsv(user_id: num)

  getStartDateInterval(timeInterval: TimeInterval): Date {
    let daysToSubtract: number = 365
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