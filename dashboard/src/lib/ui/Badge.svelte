<script lang="ts">
  import Icon from '@iconify/svelte'

  export let title = "Проработанные часы"
  export let value: string | number = "20"
  export let measure = 'часов'
  export let label = "Количество часов возросло"
  export let icon = 'mdi:clock'
</script>

<div class="bg-backgroundSecondary px-3 py-4 rounded-md shadow-md flex flex-col justify-between my-2">
  <div class="flex justify-between gap-4">
    <span class="font-bold" >{title}</span>
    <Icon {icon} class="text-primary" width="20"/>
  </div>
  <div class="font-black flex items-center gap-2 my-2">
    <span class=" text-5xl {$$props.class}">{value}</span>
    <span>{measure}</span>
  </div>
  <span>
    {label}
  </span>
</div> 