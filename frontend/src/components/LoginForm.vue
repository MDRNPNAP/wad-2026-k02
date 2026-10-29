<template>
  <div class="login-wrapper">
    <div class="login-card">
      <header class="card-header">
        <h2>Pencatat Sesi Pelatihan HR</h2>
        <p class="subtitle">Silakan masuk untuk mengakses sistem</p>
      </header>
      <div v-if="error" class="error-box" role="alert">{{ error }}</div>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="login-username">Username</label>
          <input id="login-username" v-model="username" type="text" placeholder="Masukkan username" required />
        </div>
        <div class="form-group">
          <label for="login-password">Password</label>
          <div class="password-field">
            <input
              id="login-password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Masukkan password"
              required
            />
            <button
              type="button"
              class="btn-eye"
              :title="showPassword ? 'Sembunyikan password' : 'Lihat password'"
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? '🙈' : '👁️' }}
            </button>
          </div>
        </div>
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? 'Memverifikasi...' : 'Masuk ke Sistem' }}
        </button>
      </form>
      <div class="guest-section">
        <button type="button" class="btn-guest-link" @click="$emit('guest-mode')">
          👀 Lihat Data Sesi sebagai Tamu &rarr;
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { loginApi } from '../api.js'

const emit = defineEmits(['login-success', 'guest-mode'])
const username = ref(''), password = ref(''), showPassword = ref(false)
const error = ref(''), loading = ref(false)

async function handleLogin() {
  loading.value = true; error.value = ''
  try {
    const data = await loginApi(username.value, password.value)
    emit('login-success', data.user)
    username.value = ''; password.value = ''; showPassword.value = false
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrapper { min-height: 80vh; display: grid; place-items: center; padding: 1rem; }
.login-card { background: white; padding: 2.25rem 2rem; border-radius: 12px; max-width: 420px; width: 100%; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; }
.card-header { text-align: center; margin-bottom: 1.5rem; }
.card-header h2 { font-size: 1.35rem; color: #1e293b; margin-bottom: 0.35rem; }
.subtitle { color: #64748b; font-size: 0.875rem; }
.error-box { background: #fef2f2; color: #dc2626; padding: 0.6rem 0.85rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.85rem; border: 1px solid #fecaca; }
.form-group { margin-bottom: 1rem; display: flex; flex-direction: column; gap: 0.35rem; }
.form-group label { font-size: 0.85rem; font-weight: 600; color: #334155; }
.password-field { display: flex; align-items: center; position: relative; }
.password-field input { width: 100%; padding-right: 2.5rem; }
.btn-eye { position: absolute; right: 0.5rem; background: none; border: none; font-size: 1.1rem; cursor: pointer; padding: 0.25rem; }
.btn-submit { width: 100%; padding: 0.75rem; background: #2563eb; color: white; border: none; border-radius: 6px; font-weight: 600; font-size: 0.95rem; cursor: pointer; margin-top: 0.5rem; }
.btn-submit:hover { background: #1d4ed8; }
.guest-section { margin-top: 1.5rem; text-align: center; border-top: 1px solid #f1f5f9; padding-top: 1rem; }
.btn-guest-link { background: none; border: none; color: #0284c7; font-size: 0.85rem; cursor: pointer; text-decoration: underline; }
</style>
