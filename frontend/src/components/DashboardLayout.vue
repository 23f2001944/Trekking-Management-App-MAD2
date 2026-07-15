<template>
  <div>
    <AppNavbar />
    <div class="d-flex">
      <AppSidebar />
      <main class="flex-grow-1 p-4">
        <slot />
      </main>
    </div>
  </div>
</template>

<script>
import AppNavbar from './AppNavbar.vue'
import AppSidebar from './AppSidebar.vue'

export default {
  name: 'DashboardLayout',
  components: { AppNavbar, AppSidebar }
}
</script>