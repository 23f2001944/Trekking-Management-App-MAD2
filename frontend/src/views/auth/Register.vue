<template>
<div>
    <h1>User Registration (for Trekkers only)</h1>
    <form @submit.prevent="handleRegister">
        <div>
            <label for="name">Name:</label>
            <input type="text" name="name" id="name" v-model="form.name" required>
        </div>
        <div>
            <label for="email">Email:</label>
            <input type="email" name="email" id="email" v-model="form.email" required>
        </div>
        <div>
            <label for="phone">Contact no.:</label>
            <input type="text" name="phone" id="phone" v-model="form.phone">
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" v-model="form.password" required>
        </div>
        <button type="submit">Register</button>
    </form>
    <p>
        Already have an account?
        <router-link to="/login">Login here</router-link>
    </p>
</div>
</template>


<script>
import api from '@/api/axios'

export default {
    name: "UserRegister",
    data() {
        return {
            form: { 
                name: '',
                email: '',
                phone: '',
                password: '' 
            }
        }
    },
    methods: {
        async handleRegister() {
            try {
                await api.post('/register', this.form);
                alert("Registration successful!");
                this.$router.push("/login");
            } catch (error) {
                alert(error.response?.data?.message || 'Registration failed! Please try again.');
            }
        }
    }
}
</script>