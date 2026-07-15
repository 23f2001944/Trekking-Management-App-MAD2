<template>
  <div v-if="visible">
    <div class="modal d-block" tabindex="-1">
      <div class="modal-dialog">
        <form class="modal-content" @submit.prevent="submit">
          <div class="modal-header">
            <h5 class="modal-title">Create New Trekking Staff</h5>
            <button type="button" class="btn-close" @click="$emit('close')"></button>
          </div>
          <div class="modal-body">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <div class="mb-3">
              <label class="form-label">Full Name</label>
              <input v-model="form.name" type="text" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Email Address</label>
              <input v-model="form.email" type="email" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Contact No.</label>
              <input v-model="form.phone" type="text" class="form-control">
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="form.password" type="password" class="form-control" minlength="6" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Confirm Password</label>
              <input v-model="confirmPassword" type="password" class="form-control" required>
            </div>
            <div class="alert alert-info mb-0">
              <i class="bi bi-info-circle"></i> Staff will receive their email and password as login credentials.
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? 'Creating...' : 'Create Staff' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    <div class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import api from '@/api/axios'

export default {
  name: 'StaffFormModal',
  props: { visible: Boolean },
  emits: ['close', 'saved'],
  data() {
    return { form: this.empty(), confirmPassword: '', submitting: false, error: '' }
  },
  watch: {
    visible(v) {
      if (v) Object.assign(this.$data, { form: this.empty(), confirmPassword: '', error: '' })
    }
  },
  methods: {
    empty() {
      return { name: '', email: '', phone: '', password: '' }
    },
    async submit() {
      if (this.form.password !== this.confirmPassword) {
        this.error = 'Passwords do not match'
        return
      }
      this.error = ''
      this.submitting = true
      try {
        await api.post('/admin/create-staff', this.form)
        this.$emit('saved')
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to create staff'
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>