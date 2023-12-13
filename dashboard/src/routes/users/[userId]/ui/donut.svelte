<script lang="ts">
  import {onMount} from 'svelte'
  import {page} from '$app/stores'
  import {rpc} from '$lib/client'
  import {period} from '../controller'

  let loading = true
  onMount(async () => {
    console.log($page)
    const userId = Number($page.params.userId)
  
    const events = await rpc.EventTimeInterval.getForUser(userId, $period)
    console.log(events)
  })
</script>
