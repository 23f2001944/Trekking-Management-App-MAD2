<template>
  <DashboardLayout>
    <h2 class="mb-4">My Profile</h2>

    <div v-if="loading" class="text-muted">Loading...</div>

    <div v-else class="row">
      <div class="col-md-7">
        <div class="card shadow-sm">
          <div class="card-body">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <div v-if="success" class="alert alert-success">{{ success }}</div>

            <form @submit.prevent="handleSave">
              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input v-model="form.name" type="text" class="form-control" required>
              </div>

              <div class="mb-3">
                <label class="form-label">Email</label>
                <input v-model="form.email" type="email" class="form-control" required>
              </div>

              <div class="mb-3">
                <label class="form-label">Contact No.</label>
                <input v-model="form.phone" type="text" class="form-control">
              </div>

              <hr class="my-4">

              <p class="text-muted mb-3">Leave the password fields blank to keep your current password.</p>

              <div class="mb-3">
                <label class="form-label">New Password</label>
                <input v-model="form.password" type="password" class="form-control" minlength="6">
              </div>

              <div class="mb-3">
                <label class="form-label">Confirm New Password</label>
                <input v-model="confirmPassword" type="password" class="form-control" minlength="6">
              </div>

              <button type="submit" class="btn btn-primary" :disabled="saving">
                {{ saving ? 'Saving...' : 'Save Changes' }}
              </button>
            </form>
          </div>
        </div>
      </div>

      <div class="col-md-5">
        <div class="card shadow-sm">
          <div class="card-body text-center">
            <i class="bi bi-person-circle text-primary" style="font-size: 4rem;"></i>
            <h5 class="mt-3 mb-0">{{ form.name }}</h5>
            <p class="text-muted mb-2">{{ form.email }}</p>
            <span class="badge bg-primary text-uppercase">{{ roleLabel }}</span>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'
import api from '@/api/axios'

const ROLE_LABELS = {
  admin: 'Admin',
  staff: 'Trek Staff',
  trekker: 'Trekker'
}

export default {
  name: 'ProfilePage',
  components: { DashboardLayout },
  data() {
    return {
      loading: true,
      saving: false,
      error: null,
      success: null,
      form: { name: '', email: '', phone: '', password: '' },
      confirmPassword: ''
    }
  },
  computed: {
    roleLabel() {
      return ROLE_LABELS[localStorage.getItem('role')] || 'User'
    }
  },
  async mounted() {
    await this.loadProfile()
  },
  methods: {
    async loadProfile() {
      this.loading = true
      try {
        const res = await api.get('/user/profile')
        this.form = { name: res.data.name, email: res.data.email, phone: res.data.phone || '', password: '' }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to load profile'
      } finally {
        this.loading = false
      }
    },
    async handleSave() {
      this.error = null
      this.success = null

      if (this.form.password && this.form.password !== this.confirmPassword) {
        this.error = 'Passwords do not match'
        return
      }

      this.saving = true
      try {
        const payload = {
          name: this.form.name,
          email: this.form.email,
          phone: this.form.phone
        }
        if (this.form.password) payload.password = this.form.password

        await api.put('/user/profile', payload)

        // keep navbar / sidebar in sync since they read from localStorage
        localStorage.setItem('name', this.form.name)

        this.success = 'Profile updated successfully!'
        this.form.password = ''
        this.confirmPassword = ''
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update profile'
      } finally {
        this.saving = false
      }
    }
  }
}
</script>