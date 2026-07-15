<template>
  <DashboardLayout>
    <h2 class="mb-4">Browse Treks</h2>

    <div class="row g-2 mb-3">
      <div class="col-md-4">
        <input v-model="search" type="text" class="form-control" placeholder="Search by name or location...">
      </div>
      <div class="col-md-3">
        <select v-model="difficultyFilter" class="form-select">
          <option value="">All Difficulties</option>
          <option value="Easy">Easy</option>
          <option value="Moderate">Moderate</option>
          <option value="Hard">Hard</option>
        </select>
      </div>
      <div class="col-md-2">
        <button class="btn btn-outline-secondary w-100" @click="resetFilters">Clear</button>
      </div>
    </div>

    <div v-if="loading" class="text-muted">Loading...</div>

    <div v-else class="row row-cols-1 row-cols-md-3 g-3">
      <div class="col" v-for="trek in filteredTreks" :key="trek.id">
        <TrekCard
          :trek="trek"
          :action-label="canBook(trek) ? 'Book Now' : 'Not Available'"
          :disabled="!canBook(trek)"
          @action="bookTrek"
        />
      </div>
      <p v-if="filteredTreks.length === 0" class="text-muted">No treks match your search.</p>
    </div>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'
import TrekCard from '@/components/TrekCard.vue'
import api from '@/api/axios'

export default {
  name: 'UserTreks',
  components: { DashboardLayout, TrekCard },
  data() {
    return {
      loading: true,
      treks: [],
      search: '',
      difficultyFilter: '',
    }
  },
  computed: {
    durationOptions() {
      const durations = [...new Set(this.treks.map(t => t.duration))]
      return durations.sort((a, b) => a - b)
    },
    filteredTreks() {
      const term = this.search.trim().toLowerCase()
      return this.treks.filter(trek => {
        const matchesSearch = !term
          || trek.name.toLowerCase().includes(term)
          || trek.location.toLowerCase().includes(term)
        const matchesDifficulty = !this.difficultyFilter || trek.difficulty === this.difficultyFilter
        return matchesSearch && matchesDifficulty
      })
    }
  },
  async mounted() {
    await this.loadTreks()
  },
  methods: {
    async loadTreks() {
      this.loading = true
      try {
        const res = await api.get('/treks')
        this.treks = res.data
      } catch (error) {
        alert(error.response?.data?.message || 'Failed to load treks')
      } finally {
        this.loading = false
      }
    },
    resetFilters() {
      this.search = ''
      this.difficultyFilter = ''
    },
    canBook(trek) {
      return trek.status === 'Open' && trek.available_slots > 0
    },
    async bookTrek(trek) {
      if (!this.canBook(trek)) return
      if (!confirm(`Book "${trek.name}"?`)) return
      try {
        await api.post(`/book/trek/${trek.id}`)
        alert('Trek booked successfully!')
        await this.loadTreks() // refresh slots
      } catch (error) {
        alert(error.response?.data?.message || 'Booking failed! Please try again.')
      }
    }
  }
}
</script>