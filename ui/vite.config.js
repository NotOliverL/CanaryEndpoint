import { defineConfig } from 'vite'
import tailwindcss from "@tailwindcss/vite"
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  base: '/static/ui/',
  plugins: [tailwindcss(), vue()],
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
      '/r': 'http://127.0.0.1:8000',
    },
  },
  build: {
    outDir: path.resolve(__dirname, '../frontend/static/ui'),
    emptyOutDir: true,
  }
})
