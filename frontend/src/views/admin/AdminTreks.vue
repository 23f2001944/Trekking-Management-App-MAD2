<template>
  <DashboardLayout>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Treks</h2>
      <button class="btn btn-primary" @click="openCreateModal">
        <i class="bi bi-plus-lg"></i> Add New Trek
      </button>
    </div>

    <div class="row g-2 mb-3">
      <div class="col-md-6">
        <input
          v-model="search"
          type="text"
          class="form-control"
          placeholder="Search by trek name or location..."
        >
      </div>
      <div class="col-md-3">
        <select v-model="difficultyFilter" class="form-select">
          <option value="">All Difficulties</option>
          <option value="Easy">Easy</option>
          <option value="Moderate">Moderate</option>
          <option value="Hard">Hard</option>
        </select>
      </div>
      <div class="col-md-3">
        <select v-model="statusFilter" class="form-select">
          <option value="">All Statuses</option>
          <option v-for="s in statusOptions" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="text-muted">Loading...</div>

    <div v-else class="table-responsive">
      <table class="table table-hover align-middle">
        <thead>
          <tr>
            <th>ID</th>
            <th>Trek Name</th>
            <th>Location</th>
            <th>Difficulty</th>
            <th>Duration</th>
            <th>Slots</th>
            <th>Status</th>
            <th>Assigned Staff</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="trek in filteredTreks" :key="trek.id">
            <td>{{ trek.id }}</td>
            <td>{{ trek.name }}</td>
            <td>{{ trek.location }}</td>
            <td>{{ trek.difficulty }}</td>
            <td>{{ trek.duration }} days</td>
            <td>{{ trek.available_slots }} / {{ trek.total_slots }}</td>
            <td><StatusBadge :status="trek.status" /></td>
            <td>{{ staffName(trek.assigned_staff_id) }}</td>
            <td>
              <button class="btn btn-sm btn-outline-primary me-1" @click="openEditModal(trek)">
                <i class="bi bi-pencil"></i>
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteTrek(trek)">
                <i class="bi bi-trash"></i>
              </button>
            </td>
          </tr>
          <tr v-if="filteredTreks.length === 0">
            <td colspan="9" class="text-center text-muted">No treks found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <TrekFormModal
      :visible="showModal"
      :trek="selectedTrek"
      role="admin"
      :staff-options="activeStaff"
      @close="showModal = false"
      @saved="handleSaved"
    />
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import TrekFormModal from '@/components/TrekFormModal.vue'
import api from '@/api/axios'

export default {
  name: 'AdminTreks',
  components: { DashboardLayout, StatusBadge, TrekFormModal },
  data() {
    return {
      loading: true,
      treks: [],
      staff: [],
      search: '',
      difficultyFilter: '',
      statusFilter: '',
      statusOptions: ['Pending', 'Approved', 'Open', 'Closed', 'Completed'],
      showModal: false,
      selectedTrek: null
    }
  },
  computed: {
    activeStaff() {
      return this.staff.filter(s => s.is_active)
    },
    filteredTreks() {
      const term = this.search.trim().toLowerCase()
      return this.treks.filter(trek => {
        const matchesSearch = !term
          || trek.name.toLowerCase().includes(term)
          || trek.location.toLowerCase().includes(term)
        const matchesDifficulty = !this.difficultyFilter || trek.difficulty === this.difficultyFilter
        const matchesStatus = !this.statusFilter || trek.status === this.statusFilter
        return matchesSearch && matchesDifficulty && matchesStatus
      })
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const [treksRes, staffRes] = await Promise.all([
          api.get('/treks'),
          api.get('/admin/users', { params: { role: 'staff' } })
        ])
        this.treks = treksRes.data
        this.staff = staffRes.data
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to load treks')
      } finally {
        this.loading = false
      }
    },
    staffName(staffId) {
      if (!staffId) return '—'
      const staff = this.staff.find(s => s.id === staffId)
      return staff ? staff.name : '—'
    },
    openCreateModal() {
      this.selectedTrek = null
      this.showModal = true
    },
    openEditModal(trek) {
      this.selectedTrek = trek
      this.showModal = true
    },
    async handleSaved() {
      this.showModal = false
      await this.loadData()
    },
    async deleteTrek(trek) {
      if (!confirm(`Delete trek "${trek.name}"? This cannot be undone.`)) return
      try {
        await api.delete(`/delete/trek/${trek.id}`)
        await this.loadData()
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to delete trek')
      }
    }
  }
}
</script>