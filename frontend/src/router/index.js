import { createRouter, createWebHistory } from 'vue-router'

import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import AdminTreks from '@/views/admin/AdminTreks.vue'
import AdminStaff from '@/views/admin/AdminStaff.vue'
import AdminUsers from '@/views/admin/AdminUsers.vue'
import AdminBooking from '@/views/admin/AdminBooking.vue'
import StaffDashboard from '@/views/staff/StaffDashboard.vue'
import StaffTreks from '@/views/staff/StaffTreks.vue'
import StaffParticipants from '@/views/staff/StaffParticipants.vue'
import UserDashboard from '@/views/user/UserDashboard.vue'
import UserTreks from '@/views/user/UserTreks.vue'
import UserBookings from '@/views/user/UserBookings.vue'
import UserHistory from '@/views/user/UserHistory.vue'
import Profile from '@/views/Profile.vue'


const routes = [
  { path: "/", redirect: "/login" },

  // Authentication
  { path: "/login", component: Login },
  { path: "/register", component: Register },

  // Admin
  { path: "/admin", component: AdminDashboard, meta: { role: "admin" } },
  { path: "/admin/treks", component: AdminTreks, meta: { role: "admin" } },
  { path: "/admin/staff", component: AdminStaff, meta: { role: "admin" } },
  { path: "/admin/users", component: AdminUsers, meta: { role: "admin" } },
  { path: "/admin/bookings", component: AdminBooking, meta: { role: "admin" } },

  // Staff
  { path: "/staff", component: StaffDashboard, meta: { role: "staff" } },
  { path: "/staff/treks", component: StaffTreks, meta: { role: "staff" } },
  { path: "/staff/participants", component: StaffParticipants, meta: { role: "staff" } },

  // User
  { path: "/user", component: UserDashboard, meta: { role: "trekker" } },
  { path: "/user/treks", component: UserTreks, meta: { role: "trekker" } },
  { path: "/user/bookings", component: UserBookings, meta: { role: "trekker" } },
  { path: "/user/history", component: UserHistory, meta: { role: "trekker" } },

  { path: "/profile", component: Profile, meta: { requiresAuth: true } },

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
