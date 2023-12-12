<script lang="ts">
  import type {RPCClient} from './+server'
  import {dynamicClient} from '@chord-ts/rpc/client'

  import {onMount} from 'svelte'

  const rpc = dynamicClient<RPCClient>({endpoint: '/users'})
  onMount(async () => {
    const res = await rpc.User.getAll()
    console.log(res)
  })


</script>