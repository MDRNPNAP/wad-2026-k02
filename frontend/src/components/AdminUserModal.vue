<template>
  <div v-if="isOpen" class="modal-backdrop" @click.self="handleClose">
    <div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="admin-user-title">
      <h3 id="admin-user-title">Admin: Daftarkan Pengguna Baru</h3>
      <div v-if="feedback" :class="feedbackType === 'error' ? 'error-box' : 'success-box'" role="alert">
        {{ feedback }}
      </div>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="new-username">Username</label>
          <input id="new-username" v-model="form.username" type="text" placeholder="cth: usera" required />
        </div>
        <div class="form-group">
          <label for="new-fullname">Nama Lengkap</label>
          <input id="new-fullname" v-model="form.full_name" type="text" placeholder="cth: User A" required />
        </div>
        <div class="form-group">
          <label for="new-password">Password</label>
          <div class="password-field">
            <input
              id="new-password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Minimal 6 karakter"
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
        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="handleClose">Selesai</button>
          <button type="submit" class="btn-primary" :disabled="loading">{{ loading ? 'Menyimpan...' : 'Buat Akun' }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { createUserApi } from '../api.js'

const props = defineProps({ isOpen: Boolean })
const emit = defineEmits(['close'])
const form = reactive({ username: '', full_name: '', password: '', role: 'user' })
const feedback = ref(''), feedbackType = ref(''), loading = ref(false), showPassword = ref(false)

function resetForm() {
  form.username = ''; form.full_name = ''; form.password = ''
  feedback.value = ''; showPassword.value = false
}

watch(() => props.isOpen, (val) => { if (!val) resetForm() })

async function handleSubmit() {
  loading.value = true; feedback.value = ''
  try {
    await createUserApi({ ...form })
    feedbackType.value = 'success'; feedback.value = `Akun ${form.username} berhasil dibuat!`
    form.username = ''; form.full_name = ''; form.password = ''
  } catch (err) {
    feedbackType.value = 'error'; feedback.value = err.message
  } finally {
    loading.value = false
  }
}

function handleClose() {
  resetForm()
  emit('close')
}
</script>

<style scoped>
.modal-backdrop { position: fixed; inset: 0; background: rgba(15,23,42,0.5); display: grid; place-items: center; padding: 1rem; z-index: 50; }
.modal-card { background: white; padding: 1.5rem; border-radius: 8px; max-width: 440px; width: 100%; box-shadow: 0 10px 25px rgba(0,0,0,0.15); }
.error-box { background: #fef2f2; color: #dc2626; padding: 0.5rem 0.75rem; border-radius: 6px; margin-bottom: 0.85rem; font-size: 0.85rem; }
.success-box { background: #f0fdf4; color: #16a34a; padding: 0.5rem 0.75rem; border-radius: 6px; margin-bottom: 0.85rem; font-size: 0.85rem; }
.form-group { margin-bottom: 0.75rem; display: flex; flex-direction: column; gap: 0.25rem; }
.form-group label { font-size: 0.85rem; font-weight: 600; color: #334155; }
.password-field { display: flex; align-items: center; position: relative; }
.password-field input { width: 100%; padding-right: 2.5rem; }
.btn-eye { position: absolute; right: 0.5rem; background: none; border: none; font-size: 1.1rem; cursor: pointer; padding: 0.25rem; }
.modal-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1rem; }
.btn-cancel { padding: 0.5rem 1rem; background: #f1f5f9; color: #334155; }
.btn-primary { padding: 0.5rem 1rem; background: #2563eb; color: white; }
</style>
