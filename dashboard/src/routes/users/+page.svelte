<script lang="ts">
  import {rpc} from '$lib/client'
  import {onMount} from 'svelte'

  onMount(async () => {
    const res = await rpc.User.getAll()
    console.log(res)
  })


</script>