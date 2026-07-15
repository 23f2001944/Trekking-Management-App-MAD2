<template>
  <DashboardLayout>
    <h2 class="mb-4">Staff Dashboard</h2>

    <div v-if="loading" class="text-muted">Loading...</div>

    <div v-else>
      <div class="row row-cols-1 row-cols-md-3 g-3 mb-4">
        <div class="col"><StatCard label="Assigned Treks" :value="stats.assigned_treks" icon="bi bi-signpost-2" /></div>
        <div class="col"><StatCard label="Total Participants" :value="stats.total_participants" icon="bi bi-people" /></div>
        <div class="col"><StatCard label="Ongoing Treks" :value="stats.ongoing_treks" icon="bi bi-compass" /></div>
      </div>

      <h4 class="mb-3">My Assigned Treks</h4>
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead>
            <tr>
              <th>Trek Name</th><th>Location</th><th>Difficulty</th><th>Duration</th><th>Slots</th><th>Status</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trek in treks" :key="trek.id">
              <td>{{ trek.name }}</td>
              <td>{{ trek.location }}</td>
              <td>{{ trek.difficulty }}</td>
              <td>{{ trek.duration }} days</td>
              <td>{{ trek.available_slots }} / {{ trek.total_slots }}</td>
              <td><StatusBadge :status="trek.status" /></td>
              <td>
                <button class="btn btn-sm btn-outline-primary me-1" @click="openManage(trek)">Manage</button>
                <button class="btn btn-sm btn-outline-secondary" @click="openParticipants(trek)">Participants</button>
              </td>
            </tr>
            <tr v-if="treks.length === 0">
              <td colspan="7" class="text-center text-muted">No treks assigned yet</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <TrekFormModal
      :visible="showManageModal"
      :trek="selectedTrek"
      role="staff"
      @close="showManageModal = false"
      @saved="handleSaved"
    />

    <div v-if="showParticipantsModal" class="modal d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Participants — {{ selectedTrek?.name }}</h5>
            <button type="button" class="btn-close" @click="showParticipantsModal = false"></button>
          </div>
          <div class="modal-body">
            <table class="table table-sm align-middle">
              <thead><tr><th>Name</th><th>Email</th><th>Booking Date</th><th>Status</th></tr></thead>
              <tbody>
                <tr v-for="b in participantsForSelected" :key="b.id">
                  <td>{{ b.user_name }}</td>
                  <td>{{ b.user_email }}</td>
                  <td>{{ b.booking_date }}</td>
                  <td><StatusBadge :status="b.status" /></td>
                </tr>
                <tr v-if="participantsForSelected.length === 0">
                  <td colspan="4" class="text-center text-muted">No participants yet</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showParticipantsModal = false">Close</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showParticipantsModal" class="modal-backdrop fade show"></div>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'
import StatCard from '@/components/StatCard.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import TrekFormModal from '@/components/TrekFormModal.vue'
import api from '@/api/axios'

export default {
  name: 'StaffDashboard',
  components: { DashboardLayout, StatCard, StatusBadge, TrekFormModal },
  data() {
    return {
      loading: true,
      stats: {},
      treks: [],
      bookings: [],
      showManageModal: false,
      showParticipantsModal: false,
      selectedTrek: null
    }
  },
  computed: {
    participantsForSelected() {
      if (!this.selectedTrek) return []
      return this.bookings.filter(b => b.trek_id === this.selectedTrek.id)
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const [statsRes, treksRes, bookingsRes] = await Promise.all([
          api.get('/dashboard/stats'),
          api.get('/treks'),
          api.get('/bookings')
        ])
        this.stats = statsRes.data
        this.treks = treksRes.data
        this.bookings = bookingsRes.data
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to load dashboard')
      } finally {
        this.loading = false
      }
    },
    openManage(trek) {
      this.selectedTrek = trek
      this.showManageModal = true
    },
    openParticipants(trek) {
      this.selectedTrek = trek
      this.showParticipantsModal = true
    },
    async handleSaved() {
      this.showManageModal = false
      await this.loadData()
    }
  }
}
</script>