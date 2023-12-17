import {rpc, depends} from '@chord-ts/rpc'
import {db} from '../db' 
import {managers} from './model'
import { eq} from 'drizzle-orm'

export class Managers {

  @depends()
  ctx: { session:{user:{email: string}}} | undefined

  @rpc()
  async getManagerInfo() {
    let email: string = this.ctx?.session?.user?.email ?? "";

    let manager = await db.select()
        .from(managers)
        .where(eq(managers.domainEmail, email))
        .limit(1);

    if(manager.length == 0){
        return undefined;
    }

    return manager[0];   
  }
}