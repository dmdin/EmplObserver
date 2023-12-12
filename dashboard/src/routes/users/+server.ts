import {db} from '$lib/server/db'
import {users} from '$lib/server/models/users'
import {rpc, Composer} from '@chord-ts/rpc'
import { json } from '@sveltejs/kit'
import {sveltekitMiddleware} from '@chord-ts/rpc/middlewares'

class User {
  @rpc()
  async getAll() {
    return db.select().from(users)
  }
}

const composer = new Composer({User: new User()})
composer.use(sveltekitMiddleware())

export type RPCClient = typeof composer.clientType

export async function POST(event){
  return json(await composer.exec(event))
}