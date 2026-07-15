<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary px-3">
    <span class="navbar-brand mb-0 h1">
      <i class="bi bi-signpost-split"></i>
      Trekking Management Application
    </span>

    <div class="ms-auto dropdown">
      <button
        class="btn btn-outline-light dropdown-toggle d-flex align-items-center gap-2"
        type="button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        <i class="bi bi-person-circle"></i>
        {{ userName }}
      </button>
      <ul class="dropdown-menu dropdown-menu-end">
        <li>
          <router-link class="dropdown-item" to="/profile">
            <i class="bi bi-person"></i> Profile
          </router-link>
        </li>
        <li><hr class="dropdown-divider" /></li>
        <li>
          <button class="dropdown-item text-danger" @click="logout">
            <i class="bi bi-box-arrow-right"></i> Logout
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AppNavbar',
  data() {
    return {
      userName: localStorage.getItem('name') || 'User'
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      localStorage.removeItem('name')
      this.$router.push('/login')
    }
  }
}
</script>