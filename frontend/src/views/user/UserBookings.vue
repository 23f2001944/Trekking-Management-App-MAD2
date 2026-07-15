<template>
  <DashboardLayout>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">My Bookings</h2>
      <router-link to="/user" class="btn btn-outline-secondary btn-sm">
        &larr; Back to Dashboard
      </router-link>
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
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in filteredBookings" :key="booking.id">
            <td>{{ booking.trek_name }}</td>
            <td>{{ booking.location }}</td>
            <td>{{ booking.booking_date }}</td>
            <td>{{ booking.start_date }} - {{ booking.end_date }}</td>
            <td><StatusBadge :status="booking.status" /></td>
            <td>
              <button
                v-if="booking.status === 'Booked'"
                class="btn btn-sm btn-outline-danger"
                :disabled="cancellingId === booking.id"
                @click="cancelBooking(booking)"
              >
                {{ cancellingId === booking.id ? 'Cancelling...' : 'Cancel' }}
              </button>
              <span v-else class="text-muted">&mdash;</span>
            </td>
          </tr>
          <tr v-if="filteredBookings.length === 0">
            <td colspan="6" class="text-center text-muted">No bookings found</td>
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
  name: 'UserBookings',
  components: { DashboardLayout, StatusBadge },
  data() {
    return {
      loading: true,
      bookings: [],
      search: '',
      statusFilter: '',
      cancellingId: null
    }
  },
  computed: {
    filteredBookings() {
      const term = this.search.trim().toLowerCase()
      return this.bookings.filter(b => {
        const matchesSearch = !term
          || b.trek_name.toLowerCase().includes(term)
          || b.location.toLowerCase().includes(term)
        const matchesStatus = !this.statusFilter || b.status === this.statusFilter
        return matchesSearch && matchesStatus
      })
    }
  },
  async mounted() {
    await this.loadBookings()
  },
  methods: {
    async loadBookings() {
      this.loading = true
      try {
        const res = await api.get('/bookings')
        this.bookings = res.data
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to load bookings')
      } finally {
        this.loading = false
      }
    },
    async cancelBooking(booking) {
      if (!confirm(`Cancel your booking for "${booking.trek_name}"?`)) return
      this.cancellingId = booking.id
      try {
        await api.put(`/cancel/booking/${booking.id}`)
        await this.loadBookings()
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to cancel booking')
      } finally {
        this.cancellingId = null
      }
    }
  }
}
</script>