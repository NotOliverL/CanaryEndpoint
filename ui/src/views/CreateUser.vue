<template>
    <div class="min-h-[calc(100vh-5rem)] flex items-center justify-center">

        <!-- Create User Card -->
        <div class="card bg-base-200 shadow-md w-lg mx-auto">
            <div class="card-body">
                <h2 class="card-title mb-4">Create User</h2>
                <form @submit.prevent="create" class="space-y-4">
                    <div class="form-control w-full">
                        <label class="label" for="username">
                            <span class="label-text">Username</span>
                        </label>
                        <input
                            id="username"
                            v-model="username"
                            class="input input-bordered w-full"
                            required
                        />
                    </div>

                    <div class="form-control w-full">
                        <label class="label" for="password">
                            <span class="label-text">Password</span>
                        </label>
                        <input
                            id="password"
                            type="password"
                            v-model="password"
                            class="input input-bordered w-full"
                            required
                        />
                    </div>

                    <button type="submit" class="btn btn-primary w-full">Create User</button>
                </form>

                <p v-if="message" :class="isError ? 'text-error mt-4' : 'text-success mt-4'">
                    {{ message }}
                </p>
            </div>
        </div>

    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const username = ref('')
const password = ref('')
const message = ref('')
const isError = ref(false)

const logout = async () => {
    try {
        await axios.post('/api/lauth/logout/')
    } catch (_) {}
    localStorage.removeItem('auth')
    router.push({ name: 'login' })
}

const create = async () => {
    try {
        await axios.post('/api/users/', {
            username: username.value,
            password: password.value,
        })
        message.value = 'User created'
        isError.value = false
        username.value = ''
        password.value = ''
    } catch (err) {
        isError.value = true
        message.value = err?.response?.data?.detail || 'Error creating user'
    }
}
</script>

<style scoped>
</style>
