<template>
<div>
    <h1>User Login (for all roles)</h1>
    <form @submit.prevent="handleLogin">
        <div>
            <label for="email">Email:</label>
            <input type="email" name="email" id="email" v-model="form.email" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" v-model="form.password" required>
        </div>
        <button type="submit">Login</button>
    </form>
    <p>
        Don't have an account?
        <router-link to="/register">Register here</router-link>
    </p>
</div>
</template>


<script>
import api from '@/api/axios'

export default {
    name: "UserLogin",
    data() {
        return {
            form: { 
                email: '',
                password: '' 
            }
        }
    },
    methods: {
        async handleLogin() {
            try {
                const response = await api.post('/login', this.form);
                localStorage.setItem('token', response.data.data.access_token)
                localStorage.setItem('role', response.data.data.role)
                alert('Login successful!');
                if (response.data.data.role === "admin") {
                    this.$router.push("/admin");
                }
                else if (response.data.data.role === "staff") {
                    this.$router.push("/staff");
                }
                else {
                    this.$router.push("/user");
                }
            } catch (error) {
                alert(error.response?.data?.message || 'Login failed! Please try again.');
            }
        }
    }
}
</script>