import { createApp } from 'vue'
import App from './App.vue'
import './style.css'
import router from './router'
import axios from 'axios'

const app = createApp(App)

// Configure axios to include credentials (cookies) with requests
axios.defaults.withCredentials = true
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

// Add error interceptor to handle 401 responses
axios.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            // Quickly check if we're not already on the login page
            if (router.currentRoute.value.name !== 'login') {
                // Redirect to login if any request returns 401
                window.location.href = '/login'
            }
        }
        return Promise.reject(error)
    }
)

app.use(router)
app.mount('#app')