<template>
  <DashboardLayout>
    <h2 class="mb-4">My Dashboard</h2>

    <div v-if="loading" class="text-muted">Loading...</div>

    <div v-else>
      <div class="row row-cols-1 row-cols-md-3 g-3 mb-4">
        <div class="col">
          <StatCard label="Assigned Treks" :value="stats.assigned_treks" icon="bi bi-signpost-2" />
        </div>
        <div class="col">
          <StatCard label="Total Participants" :value="stats.total_participants" icon="bi bi-people" />
        </div>
        <div class="col">
          <StatCard label="Ongoing Treks" :value="stats.ongoing_treks" icon="bi bi-signpost-split" />
        </div>
      </div>

      <h4 class="mb-3">My Assigned Treks</h4>
      <table class="table table-hover align-middle">
        <thead>
          <tr>
            <th>Trek Name</th>
            <th>Dates</th>
            <th>Participants</th>
            <th>Slots</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="trek in assignedTreks" :key="trek.id">
            <td>{{ trek.name }}</td>
            <td>{{ trek.start_date }} - {{ trek.end_date }}</td>
            <td>{{ participantCount(trek.id) }}</td>
            <td>{{ trek.available_slots }} / {{ trek.total_slots }}</td>
            <td><StatusBadge :status="trek.status" /></td>
            <td>
              <router-link
                :to="`/staff/treks/${trek.id}`"
                class="btn btn-sm"
                :class="trek.status !== 'Completed' ? 'btn-primary' : 'btn-outline-secondary'"
              >
                {{ trek.status !== 'Completed' ? 'Manage' : 'View' }}
              </router-link>
            </td>
          </tr>
          <tr v-if="assignedTreks.length === 0">
            <td colspan="6" class="text-center text-muted">No treks assigned yet</td>
          </tr>
        </tbody>
      </table>
    </div>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'
import StatCard from '@/components/StatCard.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import api from '@/api/axios'

export default {
  name: 'StaffDashboard',
  components: { DashboardLayout, StatCard, StatusBadge },
  data() {
    return {
      loading: true,
      stats: {},
      assignedTreks: [],
      bookings: []
    }
  },
  async mounted() {
    try {
      const [statsRes, treksRes, bookingsRes] = await Promise.all([
        api.get('/dashboard/stats'),
        api.get('/treks'),
        api.get('/bookings')
      ])
      this.stats = statsRes.data
      this.assignedTreks = treksRes.data
      this.bookings = bookingsRes.data
    } catch (error) {
      alert(error.response?.data?.message || 'Failed to load dashboard')
    } finally {
      this.loading = false
    }
  },
  methods: {
    participantCount(trekId) {
      return this.bookings.filter(b => b.trek_id === trekId && b.status === 'Booked').length
    }
  }
}
</script>