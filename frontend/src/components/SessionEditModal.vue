<template>
  <div v-if="isOpen && session" class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="edit-title">
      <h3 id="edit-title">Ubah Sesi: {{ session.title }}</h3>
      <p class="owner-notice">Pemilik data: <strong>{{ session.owner_name || 'System' }}</strong></p>
      <div v-if="serverError" class="server-error" role="alert">{{ serverError }}</div>
      <form @submit.prevent="handleUpdate">
        <div class="form-group">
          <label for="edit-title-input">Judul Pelatihan</label>
          <input id="edit-title-input" v-model="form.title" type="text" required />
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="edit-trainer">Pemateri</label>
            <input id="edit-trainer" v-model="form.trainer" type="text" required />
          </div>
          <div class="form-group">
            <label for="edit-dept">Departemen</label>
            <input id="edit-dept" v-model="form.department" type="text" required />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="edit-duration">Durasi (Jam)</label>
            <input id="edit-duration" v-model.number="form.duration_hours" type="number" min="1" max="40" required />
          </div>
          <div class="form-group">
            <label for="edit-capacity">Kapasitas</label>
            <input id="edit-capacity" v-model.number="form.capacity" type="number" min="1" max="500" required />
          </div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="$emit('close')">Batal</button>
          <button type="submit" class="btn-primary" :disabled="isSubmitting">
            {{ isSubmitting ? 'Menyimpan...' : 'Simpan Perubahan' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  session: Object,
  isSubmitting: Boolean,
  serverError: String
})
const emit = defineEmits(['close', 'submit'])

const form = reactive({ title: '', trainer: '', department: '', duration_hours: 4, capacity: 30 })

watch(() => props.session, (val) => {
  if (val) {
    form.title = val.title || ''
    form.trainer = val.trainer || ''
    form.department = val.department || ''
    form.duration_hours = val.duration_hours || 4
    form.capacity = val.capacity || 30
  }
}, { immediate: true })

function handleUpdate() {
  emit('submit', { ...form })
}
</script>

<style scoped>
.modal-backdrop { position: fixed; inset: 0; background: rgba(15,23,42,0.5); display: grid; place-items: center; padding: 1rem; z-index: 50; }
.modal-card { background: white; padding: 1.5rem; border-radius: 8px; max-width: 480px; width: 100%; box-shadow: 0 10px 25px rgba(0,0,0,0.15); }
.owner-notice { font-size: 0.85rem; color: #475569; margin-bottom: 0.75rem; }
.server-error { background: #fef2f2; color: #dc2626; padding: 0.5rem 0.75rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.85rem; border: 1px solid #fecaca; }
.form-group { margin-bottom: 0.75rem; display: flex; flex-direction: column; gap: 0.25rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
label { font-size: 0.85rem; font-weight: 600; color: #334155; }
.modal-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1rem; }
.btn-cancel { padding: 0.5rem 1rem; background: #f1f5f9; color: #334155; }
.btn-primary { padding: 0.5rem 1rem; background: #2563eb; color: white; }
</style>
