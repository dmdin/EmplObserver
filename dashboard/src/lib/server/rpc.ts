import {Composer} from '@chord-ts/rpc'
import {sveltekitMiddleware} from '@chord-ts/rpc/middlewares'

import {User} from '$lib/server/users/rpc'
import { EventApplication } from './eventApplications/rpc'
import { EventTimeInterval } from './timeIntervalEvents/rpc'
// Import other rpc models
export const composer = new Composer({
  User: new User(),
  EventApplication: new EventApplication(),
  EventTimeInterval: new EventTimeInterval()
})

composer.use(sveltekitMiddleware())

export type Client = typeof composer.clientType