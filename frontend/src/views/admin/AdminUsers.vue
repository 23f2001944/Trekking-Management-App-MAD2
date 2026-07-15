<template>
  <DashboardLayout>
    <h2 class="mb-4">Users (Trekkers)</h2>

    <div class="row g-2 mb-3">
      <div class="col-md-6">
        <input v-model="search" type="text" class="form-control" placeholder="Search users by name or email...">
      </div>
      <div class="col-md-3">
        <select v-model="statusFilter" class="form-select">
          <option value="">All Statuses</option>
          <option value="active">Active</option>
          <option value="blacklisted">Blacklisted</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="text-muted">Loading...</div>

    <table v-else class="table table-hover align-middle">
      <thead>
        <tr><th>ID</th><th>Name</th><th>Email</th><th>Contact</th><th>Status</th><th>Action</th></tr>
      </thead>
      <tbody>
        <tr v-for="u in filteredUsers" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.name }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.phone || '—' }}</td>
          <td><StatusBadge :status="u.is_active ? 'Active' : 'Blacklisted'" /></td>
          <td>
            <button v-if="u.is_active" class="btn btn-sm btn-outline-danger" @click="toggleStatus(u, false)">Blacklist</button>
            <button v-else class="btn btn-sm btn-outline-success" @click="toggleStatus(u, true)">Whitelist</button>
          </td>
        </tr>
        <tr v-if="filteredUsers.length === 0"><td colspan="6" class="text-center text-muted">No users found</td></tr>
      </tbody>
    </table>

    <div class="alert alert-info">
      <i class="bi bi-info-circle"></i> Blacklisted users cannot log in or book treks.
    </div>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import api from '@/api/axios'

export default {
  name: 'AdminUsers',
  components: { DashboardLayout, StatusBadge },
  data() {
    return { loading: true, users: [], search: '', statusFilter: '' }
  },
  computed: {
    filteredUsers() {
      const term = this.search.trim().toLowerCase()
      return this.users.filter(u => {
        const matchesSearch = !term || u.name.toLowerCase().includes(term) || u.email.toLowerCase().includes(term)
        const matchesStatus = !this.statusFilter || (this.statusFilter === 'active' ? u.is_active : !u.is_active)
        return matchesSearch && matchesStatus
      })
    }
  },
  async mounted() {
    await this.loadUsers()
  },
  methods: {
    async loadUsers() {
      this.loading = true
      try {
        const res = await api.get('/admin/users', { params: { role: 'trekker' } })
        this.users = res.data
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to load users')
      } finally {
        this.loading = false
      }
    },
    async toggleStatus(user, isActive) {
      const action = isActive ? 'whitelist' : 'blacklist'
      if (!confirm(`${action[0].toUpperCase() + action.slice(1)} ${user.name}?`)) return
      try {
        await api.put(`/admin/user/${user.id}/status`, { is_active: isActive })
        await this.loadUsers()
      } catch (error) {
        alert(error.response?.data?.message || `Failed to ${action} user`)
      }
    }
  }
}
</script>