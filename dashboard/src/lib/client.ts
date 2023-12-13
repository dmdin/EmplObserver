import { writable, type Writable } from 'svelte/store'
import type {Client} from './server/rpc'
import {dynamicClient} from '@chord-ts/rpc/client'

export const rpc = dynamicClient<Client>({endpoint: '/'})

export type Users = Awaited<ReturnType<typeof rpc.User.getAll>>
export const users: Writable<Users> = writable([])