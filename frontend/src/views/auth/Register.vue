<template>
  <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light py-4">
    <div class="card shadow-sm" style="width: 100%; max-width: 450px;">
      <div class="card-body p-4">
        <h4 class="text-center mb-1">Create an Account</h4>
        <p class="text-center text-muted mb-4">For Trekkers only</p>
        <form @submit.prevent="handleRegister">
          <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input type="text" id="name" class="form-control" v-model="form.name" required>
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input type="email" id="email" class="form-control" v-model="form.email" required>
          </div>
          <div class="mb-3">
            <label for="phone" class="form-label">Contact No.</label>
            <input type="text" id="phone" class="form-control" v-model="form.phone">
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" id="password" class="form-control" v-model="form.password" required>
          </div>
          <button type="submit" class="btn btn-primary w-100" :disabled="submitting">
            {{ submitting ? 'Registering...' : 'Register' }}
          </button>
        </form>
        <p class="text-center mt-3 mb-0">
          Already have an account? <router-link to="/login">Login here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api/axios'

export default {
  name: "UserRegister",
  data() {
    return {
      form: { name: '', email: '', phone: '', password: '' },
      submitting: false
    }
  },
  methods: {
    async handleRegister() {
      this.submitting = true
      try {
        await api.post('/register', this.form);
        alert("Registration successful!");
        this.$router.push("/login");
      } catch (error) {
        alert(error.response?.data?.message || 'Registration failed! Please try again.');
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>