<template>
  <DashboardLayout>
    <h2 class="mb-4">My Treks</h2>

    <div class="row g-2 mb-3">
      <div class="col-md-6">
        <input v-model="search" type="text" class="form-control" placeholder="Search by trek name or location...">
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
            <th>Registered Users</th>
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
            <td>{{ participantCount(trek.id) }}</td>
            <td>
              <button class="btn btn-sm btn-outline-primary me-1" @click="openEditModal(trek)">
                <i class="bi bi-pencil"></i> Manage
              </button>
              <button
                v-if="trek.status !== 'Completed'"
                class="btn btn-sm btn-outline-success"
                @click="markCompleted(trek)"
              >
                Mark Completed
              </button>
            </td>
          </tr>
          <tr v-if="filteredTreks.length === 0">
            <td colspan="9" class="text-center text-muted">No treks assigned to you yet</td>
          </tr>
        </tbody>
      </table>
    </div>

    <TrekFormModal
      :visible="showModal"
      :trek="selectedTrek"
      role="staff"
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
  name: 'StaffTreks',
  components: { DashboardLayout, StatusBadge, TrekFormModal },
  data() {
    return {
      loading: true,
      treks: [],
      bookings: [],
      search: '',
      statusFilter: '',
      statusOptions: ['Pending', 'Approved', 'Open', 'Closed', 'Completed'],
      showModal: false,
      selectedTrek: null
    }
  },
  computed: {
    filteredTreks() {
      const term = this.search.trim().toLowerCase()
      return this.treks.filter(trek => {
        const matchesSearch = !term
          || trek.name.toLowerCase().includes(term)
          || trek.location.toLowerCase().includes(term)
        const matchesStatus = !this.statusFilter || trek.status === this.statusFilter
        return matchesSearch && matchesStatus
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
        const [treksRes, bookingsRes] = await Promise.all([
          api.get('/treks'),
          api.get('/bookings')
        ])
        this.treks = treksRes.data
        this.bookings = bookingsRes.data
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to load treks')
      } finally {
        this.loading = false
      }
    },
    participantCount(trekId) {
      return this.bookings.filter(b => b.trek_id === trekId && b.status !== 'Cancelled').length
    },
    openEditModal(trek) {
      this.selectedTrek = trek
      this.showModal = true
    },
    async handleSaved() {
      this.showModal = false
      await this.loadData()
    },
    async markCompleted(trek) {
      if (!confirm(`Mark "${trek.name}" as completed?`)) return
      try {
        await api.put(`/update/trek/${trek.id}`, {
          status: 'Completed',
          available_slots: trek.available_slots
        })
        await this.loadData()
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to update trek status')
      }
    }
  }
}
</script>