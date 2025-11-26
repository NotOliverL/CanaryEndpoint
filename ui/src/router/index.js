import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import CreateUser from '../views/CreateUser.vue'
import axios from 'axios'

const routes = [
  { path: '/login', name: 'login', component: Login },
  { path: '/', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/users/create', name: 'create-user', component: CreateUser, meta: { requiresAuth: true } },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Simple auth check - just try to make one API request
let authCheckDone = false
let isAuthenticated = false

const checkAuth = async () => {
  if (authCheckDone) return isAuthenticated
  
  try {
    await axios.get('/api/endpoints/')
    isAuthenticated = true
    authCheckDone = true
    return true
  } catch (error) {
    isAuthenticated = false
    authCheckDone = true
    return false
  }
}

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    const authenticated = await checkAuth()
    
    if (authenticated) {
      next()
    } else {
      next({ name: 'login', query: { next: to.path } })
    }
  } else {
    next()
  }
})

export default router