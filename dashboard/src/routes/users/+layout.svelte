<script lang="ts">
  import {rpc, users} from '$lib/client'
  import {onMount} from 'svelte'

  onMount(async () => {
    $users = await rpc.User.getAll()
  })
</script>

<slot/>