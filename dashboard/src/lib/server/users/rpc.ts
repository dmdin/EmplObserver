import {rpc} from '@chord-ts/rpc'
import {db} from '../db' 
import {updateUserModel, userUpdateMessage, users} from './model'
import { eq, or } from 'drizzle-orm'

export class User {
  @rpc()
  async getAll() {
    return db.select().from(users)
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

    let insertResult = await db.insert(users).values(user).returning({ insertedId: users.id });

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
}