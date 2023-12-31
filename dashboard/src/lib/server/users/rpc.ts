import {rpc, depends} from '@chord-ts/rpc'
import {db} from '../db' 
import {updateUserModel, userUpdateMessage, users} from './model'
import { and, eq, or, sql, gt } from 'drizzle-orm'
import { userStatistic } from '../userStatistics/model'
import { managers } from '../managers/model'
import { integer } from 'drizzle-orm/pg-core'
import { TimeInterval } from '$lib/enums'
import {timeIntervalEvents} from './model'

export class User {
  @depends()
  ctx: { session:{user:{email: string}}} | undefined
  
  @rpc()
  async getAll() {

    let manager = await this.getManagerByEmail(await this.getUserEmail());

    if(manager == undefined){
      return []
    }
    else{
      return db.select({
        userId: users.id,
        domainName: users.domainName,
        domainEmail: users.domainEmail,
        sendMessagesCount: sql<number>`avg(${userStatistic.sendMessagesCount})`,
        receivedMessagesCount:  sql<number>`sum(${userStatistic.receivedMessagesCount})`,
        recipientCounts: sql<number>`avg(${userStatistic.recipientCounts})`,
        bccCount: sql<number>`avg(${userStatistic.bccCount})`,
        ccCount: sql<number>`avg(${userStatistic.ccCount})`,
        daysBetweenReceivedAndRead: sql<number>`avg(${userStatistic.daysBetweenReceivedAndRead})`,
        repliedMessagesCount: sql<number>`sum(${userStatistic.repliedMessagesCount})`,
        sentCharactersCount: sql<number>`avg(${userStatistic.sentCharactersCount})`,
        messagesOutsideWorkingHours: sql<number>`avg(${userStatistic.messagesOutsideWorkingHours})`,
        receivedToSentRatio: sql<number>`avg(${userStatistic.receivedToSentRatio})`,
        bytesReceivedToSentRatio: sql<number>`avg(${userStatistic.bytesReceivedToSentRatio})`,
        messagesWithQuestionAndNoReply: sql<number>`avg(${userStatistic.messagesWithQuestionAndNoReply})`,
        readMessagesMoreThan4Hours: sql<number>`avg(${userStatistic.readMessagesMoreThan4Hours})`,
        dismissalProbability: sql<number>`avg(${userStatistic.dismissalProbability})`
      }).from(users)
      .leftJoin(userStatistic, eq(users.id, userStatistic.user))
      .where(eq(users.managerId, manager.id))
      .groupBy(users.id)
    }

    
  }

  @rpc()
  async getForUserByDiap(user_id: number, timeInterval: TimeInterval) {
    let manager = await this.getManagerByEmail(await this.getUserEmail());
    // const startDate: Date = this.getStartDateInterval(timeInterval);

    if(manager == undefined){
      return []
    }
    else{
      return db.select({
        userId: users.id,
        domainName: users.domainName,
        domainEmail: users.domainEmail,
        dismissalProbability: sql<number>`avg(${userStatistic.dismissalProbability})`
      }).from(users)
      .leftJoin(userStatistic, eq(users.id, userStatistic.user))
      .where(eq(users.managerId, manager.id))
      .groupBy(users.id)
  }
}

@rpc()
  async getForUserStats(user_id: number, timeInterval: TimeInterval) {
    
    const startDate: Date = this.getStartDateInterval(timeInterval);

    return db.select({
      userId: users.id,
      domainName: users.domainName,
      domainEmail: users.domainEmail,
      dismissalProbability: userStatistic.dismissalProbability
    }).from(userStatistic)
    .leftJoin(users, eq(userStatistic.user, user_id))
    .where(and(eq(user_id, users.id), gt(userStatistic.startInterval, String(startDate))))
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

  @rpc()
  async create(user: updateUserModel){

    let response: userUpdateMessage = {
      userId: undefined,
      success: true,
      message: ""
    }

    if(!user.domainEmail ||
        !user.domainName)
    {
      response.message = "Доменное имя и почта обязательны для заполнения";
      response.success = false;
      return response;
    }

    
    let existedUsers = await db.select().from(users)
      .where(or(eq(users.domainName, user.domainName ?? ""), eq(users.domainEmail, user.domainEmail ?? "")));

    if(existedUsers.length > 0){
      response.message = "Пользователь с таким доменным именем или почтой уже существует";
      response.success = false;
      return response;
    }

    let manager = await this.getManagerByEmail(await this.getUserEmail());

    if(manager == undefined){
      response.message = "Неавторизированные пользователи не могу создавать сотрудников";
      response.success = false;
      return response;
    }
    
    let insertResult = await db.insert(users).values({...user, managerId: manager.id}).returning({ insertedId: users.id });

    response.message = "Пользователь успешно добавлен"
    response.userId = insertResult[0].insertedId;

    return response;
  }

  @rpc()
  async update(user: updateUserModel){

    let response: userUpdateMessage = {
      userId: undefined,
      success: true,
      message: ""
    }

    if(!user.domainEmail ||
        !user.domainName)
    {
      response.message = "Доменное имя и почта обязательны для заполнения";
      response.success = false;
      return response;
    }

    if(!user.id){
      response.message = "Id обязатьельно для запонения";
      response.success = false;
      return response;
    }

    let updateResult = await db.update(users)
      .set({ domainEmail: user.domainEmail, domainName: user.domainName })
      .where(eq(users.id, user.id))
      .returning({ updatedId: users.id });

    if(updateResult.length == 0){
      response.message = "Пользователь с переданным Id не найден";
      response.success = false;
      return response;
    }

    response.userId = user.id
    response.message = "Пользователь успешно обновлен"
    return response;
  }

  @rpc()
  async delete(userId: number){
    const deletedUserIds: { deletedId: number }[] = await db.delete(users)
      .where(eq(users.id, userId))
      .returning({ deletedId: users.id });

    let response: userUpdateMessage = {
        userId: undefined,
        success: true,
        message: ""
      }

    if(deletedUserIds.length == 0){
      response.message = "Пользователь с переданным id не найден"
      response.success = false
      return response
    }

    response.userId = userId
    response.message = "Пользователь успешно удален"

    return response;
  }

  async getUserEmail(){
    return  this.ctx?.session?.user?.email ?? "";
  }

  async getManagerByEmail(email: string){
    let manager = await db.select().from(managers).limit(1);

    if(manager.length == 0){
      return undefined;
    }

    return manager[0];
  }
}