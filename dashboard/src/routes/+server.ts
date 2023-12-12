
import { json } from '@sveltejs/kit'
import {composer} from '$lib/server/rpc'




export async function POST(event){
  return json(await composer.exec(event))
}