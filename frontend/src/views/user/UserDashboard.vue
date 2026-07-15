<template>
  <DashboardLayout>
    <h2 class="mb-4">Welcome, {{ userName }}!</h2>

    <div v-if="loading" class="text-muted">Loading...</div>

    <div v-else>
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="mb-0">Available Treks</h4>
        <router-link to="/user/treks">Browse All Treks &rarr;</router-link>
      </div>

      <div class="row row-cols-1 row-cols-md-3 g-3 mb-5">
        <div class="col" v-for="trek in availableTreks" :key="trek.id">
          <TrekCard
            :trek="trek"
            :action-label="canBook(trek) ? 'Book Now' : 'Not Available'"
            :disabled="!canBook(trek)"
            @action="bookTrek"
          />
        </div>
        <p v-if="availableTreks.length === 0" class="text-muted">
          No treks available right now.
        </p>
      </div>

      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="mb-0">My Bookings</h4>
        <router-link to="/user/bookings">View All Bookings &rarr;</router-link>
      </div>

      <table class="table table-hover align-middle">
        <thead>
          <tr>
            <th>Trek Name</th>
            <th>Booking Date</th>
            <th>Trek Dates</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in recentBookings" :key="booking.id">
            <td>{{ booking.trek_name }}</td>
            <td>{{ booking.booking_date }}</td>
            <td>{{ booking.start_date }} - {{ booking.end_date }}</td>
            <td><StatusBadge :status="booking.status" /></td>
            <td>
              <router-link to="/user/bookings" class="btn btn-sm btn-outline-primary">
                View Details
              </router-link>
            </td>
          </tr>
          <tr v-if="recentBookings.length === 0">
            <td colspan="5" class="text-center text-muted">No bookings yet</td>
          </tr>
        </tbody>
      </table>
    </div>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'
import TrekCard from '@/components/TrekCard.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import api from '@/api/axios'

export default {
  name: 'UserDashboard',
  components: { DashboardLayout, TrekCard, StatusBadge },
  data() {
    return {
      loading: true,
      userName: localStorage.getItem('name') || 'Trekker',
      availableTreks: [],
      recentBookings: []
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      try {
        const [treksRes, bookingsRes] = await Promise.all([
          api.get('/treks'),
          api.get('/bookings')
        ])
        // dashboard only teases a few - full browsing happens on /user/treks
        this.availableTreks = treksRes.data.slice(0, 3)
        this.recentBookings = bookingsRes.data.slice(0, 5)
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to load dashboard')
      } finally {
        this.loading = false
      }
    },
    canBook(trek) {
      return trek.status === 'Open' && trek.available_slots > 0
    },
    async bookTrek(trek) {
      if (!this.canBook(trek)) return
      try {
        await api.post(`/book/trek/${trek.id}`)
        alert('Trek booked successfully!')
        await this.loadData() // refresh slots + bookings
      } catch (error) {
        alert(error.response?.data?.message || 'Booking failed! Please try again.')
      }
    }
  }
}
</script>