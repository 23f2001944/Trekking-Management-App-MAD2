<template>
  <DashboardLayout>
    <h2 class="mb-4">Bookings</h2>

    <div class="row g-2 mb-3">
      <div class="col-md-6">
        <input v-model="search" type="text" class="form-control" placeholder="Search by trekker or trek name...">
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
            <th>Booking ID</th>
            <th>Trekker</th>
            <th>Trek</th>
            <th>Location</th>
            <th>Trek Dates</th>
            <th>Booking Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in filteredBookings" :key="b.id">
            <td>{{ b.id }}</td>
            <td>{{ b.user_name }}<br><small class="text-muted">{{ b.user_email }}</small></td>
            <td>{{ b.trek_name }}</td>
            <td>{{ b.location }}</td>
            <td>{{ b.start_date }} - {{ b.end_date }}</td>
            <td>{{ b.booking_date }}</td>
            <td><StatusBadge :status="b.status" /></td>
          </tr>
          <tr v-if="filteredBookings.length === 0">
            <td colspan="7" class="text-center text-muted">No bookings found</td>
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
  name: 'AdminBookings',
  components: { DashboardLayout, StatusBadge },
  data() {
    return { loading: true, bookings: [], search: '', statusFilter: '' }
  },
  computed: {
    filteredBookings() {
      const term = this.search.trim().toLowerCase()
      return this.bookings.filter(b => {
        const matchesSearch = !term
          || (b.user_name || '').toLowerCase().includes(term)
          || b.trek_name.toLowerCase().includes(term)
        const matchesStatus = !this.statusFilter || b.status === this.statusFilter
        return matchesSearch && matchesStatus
      })
    }
  },
  async mounted() {
    try {
      const res = await api.get('/bookings')
      this.bookings = res.data
    } catch (error) {
      alert(error.response?.data?.message || 'Failed to load bookings')
    } finally {
      this.loading = false
    }
  }
}
</script>