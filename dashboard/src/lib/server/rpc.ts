import {Composer} from '@chord-ts/rpc'
import {sveltekitMiddleware} from '@chord-ts/rpc/middlewares'

import {User} from '$lib/server/users/rpc'
// Import other rpc models
export const composer = new Composer({
  User: new User()
})

composer.use(sveltekitMiddleware())

export type Client = typeof composer.clientType