<template>
  <div class="d-flex align-items-center justify-content-center vh-100 bg-light">
    <div class="card shadow-sm" style="width: 100%; max-width: 400px;">
      <div class="card-body p-4">
        <h3 class="text-center text-primary mb-1"><i class="bi bi-signpost-split"></i></h3>
        <h4 class="text-center mb-4">Login</h4>
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input type="email" id="email" class="form-control" v-model="form.email" required>
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" id="password" class="form-control" v-model="form.password" required>
          </div>
          <button type="submit" class="btn btn-primary w-100" :disabled="submitting">
            {{ submitting ? 'Logging in...' : 'Login' }}
          </button>
        </form>
        <p class="text-center mt-3 mb-0">
          Don't have an account? <router-link to="/register">Register here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api/axios'

export default {
  name: "UserLogin",
  data() {
    return { form: { email: '', password: '' }, submitting: false }
  },
  methods: {
    async handleLogin() {
      this.submitting = true
      try {
        const response = await api.post('/login', this.form);
        localStorage.setItem('token', response.data.data.access_token)
        localStorage.setItem('role', response.data.data.role)
        localStorage.setItem('name', response.data.data.name)
        if (response.data.data.role === "admin") this.$router.push("/admin")
        else if (response.data.data.role === "staff") this.$router.push("/staff")
        else this.$router.push("/user")
      } catch (error) {
        alert(error.response?.data?.message || 'Login failed! Please try again.')
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>