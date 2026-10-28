<template>
  <div v-if="isOpen" class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="login-title">
      <h3 id="login-title">Masuk ke Sistem HR</h3>
      <div v-if="error" class="error-box" role="alert">{{ error }}</div>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="login-username">Username</label>
          <input id="login-username" v-model="username" type="text" placeholder="Username" required />
        </div>
        <div class="form-group">
          <label for="login-password">Password</label>
          <input id="login-password" v-model="password" type="password" placeholder="Password" required />
        </div>
        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="$emit('close')">Batal</button>
          <button type="submit" class="btn-primary" :disabled="loading">{{ loading ? 'Masuk...' : 'Login' }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { loginApi } from '../api.js'

defineProps({ isOpen: Boolean })
const emit = defineEmits(['close', 'login-success'])
const username = ref(''), password = ref(''), error = ref(''), loading = ref(false)

async function handleLogin() {
  loading.value = true; error.value = ''
  try {
    const data = await loginApi(username.value, password.value)
    emit('login-success', data.user)
    emit('close')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-backdrop { position: fixed; inset: 0; background: rgba(15,23,42,0.5); display: grid; place-items: center; padding: 1rem; z-index: 50; }
.modal-card { background: white; padding: 1.5rem; border-radius: 8px; max-width: 400px; width: 100%; box-shadow: 0 10px 25px rgba(0,0,0,0.15); }
.error-box { background: #fef2f2; color: #dc2626; padding: 0.5rem 0.75rem; border-radius: 6px; margin-bottom: 0.85rem; font-size: 0.85rem; }
.form-group { margin-bottom: 0.85rem; display: flex; flex-direction: column; gap: 0.25rem; }
.form-group label { font-size: 0.85rem; font-weight: 600; color: #334155; }
.modal-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1rem; }
.btn-cancel { padding: 0.5rem 1rem; background: #f1f5f9; color: #334155; }
.btn-primary { padding: 0.5rem 1rem; background: #2563eb; color: white; }
</style>
