<template>
  <div v-if="isOpen" class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="form-title">
      <h3 id="form-title">Tambah Sesi Pelatihan Baru</h3>
      <div v-if="serverError" class="server-error" role="alert">{{ serverError }}</div>
      <form @submit.prevent="handleSubmit" novalidate>
        <div class="form-group">
          <label for="title">Judul Pelatihan</label>
          <input id="title" v-model="form.title" type="text" placeholder="cth: Data Literacy" required />
          <span v-if="errors.title" class="field-error">{{ errors.title }}</span>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="trainer">Pemateri / Trainer</label>
            <input id="trainer" v-model="form.trainer" type="text" placeholder="Nama trainer" required />
            <span v-if="errors.trainer" class="field-error">{{ errors.trainer }}</span>
          </div>
          <div class="form-group">
            <label for="department">Departemen</label>
            <input id="department" v-model="form.department" type="text" placeholder="cth: Human Resources" required />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="date">Tanggal Pelaksanaan</label>
            <input id="date" v-model="form.date" type="date" required />
            <span v-if="errors.date" class="field-error">{{ errors.date }}</span>
          </div>
          <div class="form-group">
            <label for="duration">Durasi (Jam)</label>
            <input id="duration" v-model.number="form.duration_hours" type="number" min="1" max="40" required />
          </div>
          <div class="form-group">
            <label for="capacity">Kapasitas</label>
            <input id="capacity" v-model.number="form.capacity" type="number" min="1" max="500" required />
          </div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="$emit('close')">Batal</button>
          <button type="submit" class="btn-primary" :disabled="isSubmitting">
            {{ isSubmitting ? 'Menyimpan...' : 'Simpan Sesi' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

defineProps({ isOpen: Boolean, isSubmitting: Boolean, serverError: String })
const emit = defineEmits(['close', 'submit'])

const form = reactive({ title: '', trainer: '', department: 'All Departments', date: '', duration_hours: 4, capacity: 30, status: 'Scheduled' })
const errors = reactive({ title: '', trainer: '', date: '' })

function validate() {
  errors.title = form.title.trim().length < 3 ? 'Judul minimal 3 karakter' : ''
  errors.trainer = form.trainer.trim().length < 3 ? 'Nama trainer minimal 3 karakter' : ''
  errors.date = !form.date ? 'Tanggal wajib diisi' : ''
  return !errors.title && !errors.trainer && !errors.date
}

function handleSubmit() {
  if (validate()) emit('submit', { ...form })
}
</script>

<style scoped>
.modal-backdrop { position: fixed; inset: 0; background: rgba(15,23,42,0.5); display: grid; place-items: center; padding: 1rem; z-index: 50; }
.modal-card { background: white; padding: 1.5rem; border-radius: 8px; max-width: 520px; width: 100%; box-shadow: 0 10px 25px rgba(0,0,0,0.15); }
.server-error { background: #fef2f2; color: #dc2626; padding: 0.5rem 0.75rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.875rem; }
.form-group { margin-bottom: 0.85rem; display: flex; flex-direction: column; gap: 0.25rem; }
.form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 0.75rem; }
label { font-size: 0.85rem; font-weight: 600; color: #334155; }
.field-error { color: #dc2626; font-size: 0.75rem; }
.modal-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1rem; }
.btn-cancel { padding: 0.5rem 1rem; background: #f1f5f9; color: #334155; }
.btn-primary { padding: 0.5rem 1rem; background: #2563eb; color: white; }
.btn-primary:hover { background: #1d4ed8; }
</style>
