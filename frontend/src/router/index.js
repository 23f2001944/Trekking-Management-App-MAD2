import { createRouter, createWebHistory } from 'vue-router'

import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import StaffDashboard from '@/views/staff/StaffDashboard.vue'
import UserDashboard from '@/views/user/UserDashboard.vue'


const routes = [
  { path: "/", redirect: "/login" },

  // Authentication
  { path: "/login", component: Login },
  { path: "/register", component: Register },

  // Admin
  { path: "/admin", component: AdminDashboard, meta: { role: "admin" } },

  // Staff
  { path: "/staff", component: StaffDashboard, meta: { role: "staff" } },

  // User
  { path: "/user", component: UserDashboard, meta: { role: "trekker" } },

  { path: "/:pathMatch(.*)*", redirect: "/login" }  // to handle invalid urls
];

const router = createRouter({ history: createWebHistory(import.meta.env.BASE_URL), routes })

router.beforeEach((to) => {
  const role = localStorage.getItem('role')
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) return '/login'
  if (to.meta.role && to.meta.role !== role) return '/login'
  return true
})

export default router
