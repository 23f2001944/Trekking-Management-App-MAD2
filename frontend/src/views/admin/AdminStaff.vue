<template>
  <DashboardLayout>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Trekking Staff</h2>
      <button class="btn btn-primary" @click="showModal = true">
        <i class="bi bi-plus-lg"></i> Add New Staff
      </button>
    </div>

    <div class="row g-2 mb-3">
      <div class="col-md-6">
        <input v-model="search" type="text" class="form-control" placeholder="Search trekking staff...">
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
        <tr v-for="s in filteredStaff" :key="s.id">
          <td>{{ s.id }}</td>
          <td>{{ s.name }}</td>
          <td>{{ s.email }}</td>
          <td>{{ s.phone || '—' }}</td>
          <td><StatusBadge :status="s.is_active ? 'Active' : 'Blacklisted'" /></td>
          <td>
            <button v-if="s.is_active" class="btn btn-sm btn-outline-danger" @click="toggleStatus(s, false)">Blacklist</button>
            <button v-else class="btn btn-sm btn-outline-success" @click="toggleStatus(s, true)">Whitelist</button>
          </td>
        </tr>
        <tr v-if="filteredStaff.length === 0"><td colspan="6" class="text-center text-muted">No trekking staff found</td></tr>
      </tbody>
    </table>

    <div class="alert alert-info">
      <i class="bi bi-info-circle"></i> Blacklisted staff cannot login or manage treks.
    </div>

    <StaffFormModal :visible="showModal" @close="showModal = false" @saved="handleSaved" />
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import StaffFormModal from '@/components/StaffFormModal.vue'
import api from '@/api/axios'

export default {
  name: 'AdminStaff',
  components: { DashboardLayout, StatusBadge, StaffFormModal },
  data() {
    return { loading: true, staff: [], search: '', statusFilter: '', showModal: false }
  },
  computed: {
    filteredStaff() {
      const term = this.search.trim().toLowerCase()
      return this.staff.filter(s => {
        const matchesSearch = !term || s.name.toLowerCase().includes(term) || s.email.toLowerCase().includes(term)
        const matchesStatus = !this.statusFilter || (this.statusFilter === 'active' ? s.is_active : !s.is_active)
        return matchesSearch && matchesStatus
      })
    }
  },
  async mounted() {
    await this.loadStaff()
  },
  methods: {
    async loadStaff() {
      this.loading = true
      try {
        const res = await api.get('/admin/users', { params: { role: 'staff' } })
        this.staff = res.data
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to load trekking staff')
      } finally {
        this.loading = false
      }
    },
    async handleSaved() {
      this.showModal = false
      await this.loadStaff()
    },
    async toggleStatus(member, isActive) {
      const action = isActive ? 'whitelist' : 'blacklist'
      if (!confirm(`${action[0].toUpperCase() + action.slice(1)} ${member.name}?`)) return
      try {
        await api.put(`/admin/user/${member.id}/status`, { is_active: isActive })
        await this.loadStaff()
      } catch (error) {
        alert(error.response?.data?.message || `Failed to ${action} staff`)
      }
    }
  }
}
</script>