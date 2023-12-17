<script>
  import {goto} from '$app/navigation'
  import {page} from '$app/stores'


  function redirect() {
    if ($page.data.session) {
      goto('/users')
    } else {
      goto('/login')
    }
  }
</script>


<div class="w-full h-[1000px] flex flex-col items-center justify-center">
  <h1 class="text-5xl font-black">Добро пожаловать</h1>
  <h2 class="my-6 italic text-xl font-bold">в сервис оценки вовлеченности сотрудника</h2>
  <button on:click={redirect} class="btn btn-xl btn-primary">Начать работу</button>
</div>