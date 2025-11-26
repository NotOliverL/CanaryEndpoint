<template>
    <header class="navbar bg-base-300 px-4 mb-2 shadow-m flex items-center">
        <div class="flex-1 flex items-center">
            <img class="w-8 h-8 mr-2 pointer-events-none select-none" src="../assets/Picture 1.png" alt="logo">
            <a class="text-xl font-bold cursor-default select-none">Canary Endpoint</a>
        </div>
        <div class="flex-none">
            <ul class="menu menu-horizontal px-1 gap-1">
                 <li>
                    <button
                        class="hover:bg-base-200 px-2 py-1 rounded"
                        @click="toggleTheme"
                        :title="`Current: ${currentTheme === 'winter' ? 'Light' : 'Dark'} - Click to switch`"
                    >
                        {{ currentTheme === 'winter' ? '🌙' : '☀️' }}
                    </button>
                </li>               
                <li>
                    <router-link to="/dashboard" class="hover:bg-base-200 px-2 py-1 rounded">
                    Dashboard
                    </router-link>
                </li>
                <li>
                    <router-link to="/users/create" class="hover:bg-base-200 px-2 py-1 rounded">
                    Create User
                    </router-link>
                </li>
                <li>
                    <button class="bg-red-400 hover:bg-red-500 px-2 py-1 rounded text-sm font-semibold ml-1" @click="logout">Logout</button>
                </li>
            </ul>
        </div>
    </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const currentTheme = ref('business')

const applyTheme = (theme) => {
    document.documentElement.setAttribute('data-theme', theme)
    currentTheme.value = theme
    localStorage.setItem('theme', theme)
}

const getSystemTheme = () => {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'business' : 'winter'
}

const toggleTheme = () => {
    const newTheme = currentTheme.value === 'winter' ? 'business' : 'winter'
    applyTheme(newTheme)
}

onMounted(() => {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
        applyTheme(savedTheme)
    } else {
        const systemTheme = getSystemTheme()
        applyTheme(systemTheme)
    }
})

const getCookie = (name) => {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim()
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}

const logout = async () => {
    try {
        const csrftoken = getCookie('csrftoken')
        await axios.post('/api/logout/', {}, {
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
    } catch (error) {
        console.error('Logout failed:', error)
    }
    cookieStore.delete('sessionid')
    cookieStore.delete('csrftoken')
    router.push({ name: 'login' })
}
</script>