<template>
  <DashboardLayout>
    <h2 class="mb-4">Dashboard</h2>

    <div v-if="loading" class="text-muted">Loading...</div>

    <div v-else>
      <div class="row row-cols-1 row-cols-md-4 g-3 mb-4">
        <div class="col">
          <StatCard label="Total Treks" :value="stats.total_treks" icon="bi bi-signpost-2" />
        </div>
        <div class="col">
          <StatCard label="Total Users (Trekkers)" :value="stats.total_users" icon="bi bi-people" />
        </div>
        <div class="col">
          <StatCard label="Total Trekking Staff" :value="stats.total_staff" icon="bi bi-person-badge" />
        </div>
        <div class="col">
          <StatCard label="Total Bookings" :value="stats.total_bookings" icon="bi bi-journal-check" />
        </div>
      </div>

      <h4 class="mb-3">Recent Bookings</h4>
      <table class="table table-hover align-middle">
        <thead>
          <tr>
            <th>Booking ID</th>
            <th>User (Trekker)</th>
            <th>Trek</th>
            <th>Booking Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in recentBookings" :key="booking.id">
            <td>{{ booking.id }}</td>
            <td>{{ booking.user_name }}</td>
            <td>{{ booking.trek_name }}</td>
            <td>{{ booking.booking_date }}</td>
            <td><StatusBadge :status="booking.status" /></td>
          </tr>
          <tr v-if="recentBookings.length === 0">
            <td colspan="5" class="text-center text-muted">No bookings yet</td>
          </tr>
        </tbody>
      </table>

      <router-link to="/admin/bookings">View All Bookings &rarr;</router-link>
    </div>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'
import StatCard from '@/components/StatCard.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import api from '@/api/axios'

export default {
  name: 'AdminDashboard',
  components: { DashboardLayout, StatCard, StatusBadge },
  data() {
    return {
      loading: true,
      stats: {},
      recentBookings: []
    }
  },
  async mounted() {
    try {
      const [statsRes, bookingsRes] = await Promise.all([
        api.get('/dashboard/stats'),
        api.get('/bookings')
      ])
      this.stats = statsRes.data
      // /api/bookings already comes back sorted newest-first, just take the top 5
      this.recentBookings = bookingsRes.data.slice(0, 5)
    } catch (error) {
      alert(error.response?.data?.message || 'Failed to load dashboard')
    } finally {
      this.loading = false
    }
  }
}
</script>