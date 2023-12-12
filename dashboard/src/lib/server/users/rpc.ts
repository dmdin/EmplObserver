import {rpc} from '@chord-ts/rpc'
import {db} from '../db' 
import {users} from './model'

export class User {
  @rpc()
  async getAll() {
    return db.select().from(users)
  }
}