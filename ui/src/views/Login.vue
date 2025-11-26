<template>
    <!-- LOGO -->
    <div class="flex flex-col items-center justify-center min-h-screen px-6 py-8">
        <a href="#" class="flex items-center mb-6 text-2xl font-semibold">
            <img class="w-8 h-8 mr-2" src="../assets/Picture 1.png" alt="logo">
            Canary Endpoint
        </a>

        <!-- CARD -->
        <div class="card w-full max-w-md bg-base-300 shadow-xl">
            <div class="card-body">
                <h1 class="card-title text-center">Sign in to your account</h1>

                <!-- LOGIN FORM -->
                <form @submit.prevent="login" class="form-control gap-4">
                    <div class="mb-4">
                        <label for="username" class="label">
                            <span class="label-text">Username</span>
                        </label>
                        <input 
                            v-model="username"
                            type="text" 
                            id="username" 
                            placeholder="Username" 
                            class="input input-bordered w-full" 
                            required 
                        />
                    </div>

                    <div class="mb-4">
                        <label for="password" class="label">
                            <span class="label-text">Password</span>
                        </label>
                        <input 
                            v-model="password"
                            type="password" 
                            id="password" 
                            placeholder="••••••••" 
                            class="input input-bordered w-full" 
                            required 
                        />
                    </div>

                    <button type="submit" class="btn btn-primary w-full" :disabled="loading">
                        {{ loading ? 'Signing in...' : 'Sign in' }}
                    </button>

                    <div v-if="error" class="alert alert-error mt-4">
                        <span>{{ error }}</span>
                    </div>

                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

onMounted(async () => {
    try {
        // Check if user is already authenticated
        await axios.get('/api/verify-session/')
        router.push({ name: 'dashboard' })
    } catch {
        // Not authenticated, stay on login page
    }
})

const login = async () => {
    loading.value = true
    error.value = ''
    
    try {
        await axios.post('/api/login/', {
            username: username.value,
            password: password.value,
        })
        
        // Redirect to intended page or dashboard
        const redirect = route.query.next || '/'
        router.push(redirect)
    } catch (err) {
        error.value = err.response?.data?.detail || 'Invalid credentials'
        console.error('Login error:', err)
    } finally {
        loading.value = false
    }
}
</script>