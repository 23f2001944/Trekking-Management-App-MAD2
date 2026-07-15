<template>
  <div class="bg-light border-end vh-100 p-3" style="width: 230px;">
    <div class="list-group list-group-flush">
      <router-link
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        class="list-group-item list-group-item-action d-flex align-items-center gap-2"
        :class="{ active: $route.path === link.to }"
      >
        <i :class="link.icon"></i>
        {{ link.label }}
      </router-link>
    </div>
  </div>
</template>

<script>
const LINKS_BY_ROLE = {
  admin: [
    { label: 'Dashboard', to: '/admin', icon: 'bi bi-speedometer2' },
    { label: 'Treks', to: '/admin/treks', icon: 'bi bi-signpost-2' },
    { label: 'Trekking Staff', to: '/admin/staff', icon: 'bi bi-people' },
    { label: 'Users (Trekkers)', to: '/admin/users', icon: 'bi bi-person-lines-fill' },
    { label: 'Bookings', to: '/admin/bookings', icon: 'bi bi-journal-check' },
    { label: 'Profile', to: '/profile', icon: 'bi bi-person-circle' }
  ],
  staff: [
    { label: 'Dashboard', to: '/staff', icon: 'bi bi-speedometer2' },
    { label: 'My Treks', to: '/staff/treks', icon: 'bi bi-signpost-2' },
    { label: 'Participants', to: '/staff/participants', icon: 'bi bi-people' },
    { label: 'Profile', to: '/profile', icon: 'bi bi-person-circle' }
  ],
  trekker: [
    { label: 'Dashboard', to: '/user', icon: 'bi bi-speedometer2' },
    { label: 'Browse Treks', to: '/user/treks', icon: 'bi bi-compass' },
    { label: 'My Bookings', to: '/user/bookings', icon: 'bi bi-journal-check' },
    { label: 'History', to: '/user/history', icon: 'bi bi-clock-history' },
    { label: 'Profile', to: '/profile', icon: 'bi bi-person-circle' }
  ]
}

export default {
  name: 'AppSidebar',
  data() {
    return {
      links: LINKS_BY_ROLE[localStorage.getItem('role')] || []
    }
  }
}
</script>