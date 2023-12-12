import type {Client} from './server/rpc'
import {dynamicClient} from '@chord-ts/rpc/client'

export const rpc = dynamicClient<Client>({endpoint: '/'})