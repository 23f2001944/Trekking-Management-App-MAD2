<template>
  <DashboardLayout>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Trekking History</h2>
      <div class="d-flex gap-2">
        <button class="btn btn-outline-primary btn-sm" :disabled="loading || history.length === 0 || exporting" @click="exportCsv">
          <i class="bi bi-download"></i> {{ exporting ? 'Exporting...' : 'Export CSV' }}
        </button>
        <router-link to="/user" class="btn btn-outline-secondary btn-sm">
          &larr; Back to Dashboard
        </router-link>
      </div>
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
        <select v-model="statusFilter" class="form-select">
          <option value="">All Statuses</option>
          <option value="Booked">Booked</option>
          <option value="Cancelled">Cancelled</option>
          <option value="Completed">Completed</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="text-muted">Loading...</div>

    <div v-else class="table-responsive">
      <table class="table table-hover align-middle">
        <thead>
          <tr>
            <th>Trek Name</th>
            <th>Location</th>
            <th>Booking Date</th>
            <th>Trek Dates</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in filteredHistory" :key="entry.id">
            <td>{{ entry.trek_name }}</td>
            <td>{{ entry.location }}</td>
            <td>{{ entry.booking_date }}</td>
            <td>{{ entry.start_date }} - {{ entry.end_date }}</td>
            <td><StatusBadge :status="entry.status" /></td>
          </tr>
          <tr v-if="filteredHistory.length === 0">
            <td colspan="5" class="text-center text-muted">No trekking history yet</td>
          </tr>
        </tbody>
      </table>
    </div>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import api from '@/api/axios'

export default {
  name: 'UserHistory',
  components: { DashboardLayout, StatusBadge },
  data() {
    return {
      loading: true,
      history: [],
      search: '',
      statusFilter: '',
      exporting: false
    }
  },
  computed: {
    filteredHistory() {
      const term = this.search.trim().toLowerCase()
      return this.history.filter(entry => {
        const matchesSearch = !term
          || entry.trek_name.toLowerCase().includes(term)
          || entry.location.toLowerCase().includes(term)
        const matchesStatus = !this.statusFilter || entry.status === this.statusFilter
        return matchesSearch && matchesStatus
      })
    }
  },
  async mounted() {
    await this.loadHistory()
  },
  methods: {
    async loadHistory() {
      this.loading = true
      try {
        // /api/bookings already returns the full history for the logged-in trekker,
        // sorted newest-first by the backend
        const res = await api.get('/bookings')
        this.history = res.data
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to load trekking history')
      } finally {
        this.loading = false
      }
    },

    async exportCsv() {
      this.exporting = true
      try {
        const res = await api.post('/export/history')
        this.pollExportStatus(res.data.task_id)
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to start export')
        this.exporting = false
      }
    },

    pollExportStatus(taskId) {
      const interval = setInterval(async () => {
        try {
          const res = await api.get(`/export/status/${taskId}`)
          if (res.data.status === 'done') {
            clearInterval(interval)
            await this.downloadExport(res.data.filename)
            this.exporting = false
          } else if (res.data.status === 'failed') {
            clearInterval(interval)
            alert('Export failed. Please try again.')
            this.exporting = false
          }
        } catch (error) {
          clearInterval(interval)
          this.exporting = false
        }
      }, 2000)
    },

    async downloadExport(filename) {
      const res = await api.get(`/export/download/${filename}`, { responseType: 'blob' })
      const url = URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      link.click()
      URL.revokeObjectURL(url)
      alert('Export ready! CSV downloaded.')
    }
  }
}
</script>