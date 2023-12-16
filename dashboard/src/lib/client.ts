import { writable, derived, type Writable } from 'svelte/store'
import type {Client} from './server/rpc'
import {dynamicClient} from '@chord-ts/rpc/client'
import { browser } from '$app/environment'
export const rpc = dynamicClient<Client>({endpoint: '/'})

export const theme: Writable<'light' | 'dark'> = writable();


function toRGB(color: string) {
  return `rgb(${color})`

}
export const colors = derived([theme], ([$theme], set) => {
  if (!browser || !theme) return
  const element = document.getElementById('theme-root')!
  setTimeout(() => {
    const style = getComputedStyle(element)
    const bp = toRGB(style.getPropertyValue('--backgroundPrimary'))
    const c1 = toRGB(style.getPropertyValue('--content1'))
    const s = toRGB(style.getPropertyValue('--secondary'))

    set({
      bp,
      c1,
      s
    })
  }, 100) 
}) 


export type Users = Awaited<ReturnType<typeof rpc.User.getAll>>
export const users: Writable<Users> = writable([])

export type Manager = Awaited<ReturnType<typeof rpc.Managers.getManagerInfo>>
export const manager: Writable<Manager> = writable()