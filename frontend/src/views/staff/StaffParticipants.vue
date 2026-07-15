<template>
  <DashboardLayout>
    <h2 class="mb-4">Participants</h2>

    <div class="row g-2 mb-3">
      <div class="col-md-6">
        <select v-model="selectedTrekId" class="form-select">
          <option :value="null">Select a trek...</option>
          <option v-for="trek in treks" :key="trek.id" :value="trek.id">
            {{ trek.name }} ({{ trek.location }})
          </option>
        </select>
      </div>
      <div class="col-md-4">
        <input v-model="search" type="text" class="form-control" placeholder="Search participants...">
      </div>
    </div>

    <div v-if="loading" class="text-muted">Loading...</div>

    <div v-else-if="!selectedTrekId" class="alert alert-info">
      <i class="bi bi-info-circle"></i> Select a trek above to view its registered participants.
    </div>

    <table v-else class="table table-hover align-middle">
      <thead>
        <tr>
          <th>Booking ID</th>
          <th>Participant</th>
          <th>Contact</th>
          <th>Booking Date</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="b in filteredParticipants" :key="b.id">
          <td>{{ b.id }}</td>
          <td>{{ b.user_name }}</td>
          <td>{{ b.user_email || '—' }}</td>
          <td>{{ b.booking_date }}</td>
          <td><StatusBadge :status="b.status" /></td>
        </tr>
        <tr v-if="filteredParticipants.length === 0">
          <td colspan="5" class="text-center text-muted">No participants registered for this trek</td>
        </tr>
      </tbody>
    </table>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import api from '@/api/axios'

export default {
  name: 'StaffParticipants',
  components: { DashboardLayout, StatusBadge },
  data() {
    return {
      loading: true,
      treks: [],
      bookings: [],
      selectedTrekId: null,
      search: ''
    }
  },
  computed: {
    filteredParticipants() {
      const term = this.search.trim().toLowerCase()
      return this.bookings.filter(b => {
        const matchesTrek = b.trek_id === this.selectedTrekId
        const matchesSearch = !term || b.user_name.toLowerCase().includes(term)
        return matchesTrek && matchesSearch
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
        alert(error.response?.data?.message || 'Failed to load participants')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>