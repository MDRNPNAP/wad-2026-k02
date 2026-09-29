<template>
  <div v-if="state === 'loading'" class="feedback-box state-loading" role="status">
    <div class="spinner" aria-hidden="true"></div>
    <p>Memuat data sesi pelatihan...</p>
  </div>

  <div v-else-if="state === 'error'" class="feedback-box state-error" role="alert">
    <p class="error-msg">{{ errorMessage || 'Terjadi kesalahan saat memuat data.' }}</p>
    <button type="button" class="btn-retry" @click="$emit('retry')">
      🔄 Coba Lagi
    </button>
  </div>

  <div v-else-if="state === 'empty'" class="feedback-box state-empty">
    <p>Belum ada sesi pelatihan yang ditemukan.</p>
  </div>
</template>

<script setup>
defineProps({
  state: { type: String, required: true },
  errorMessage: { type: String, default: '' }
})
defineEmits(['retry'])
</script>

<style scoped>
.feedback-box {
  padding: 2.5rem 1rem;
  text-align: center;
  border-radius: 8px;
  background: #ffffff;
  border: 1px dashed #cbd5e1;
  margin: 1.5rem 0;
}
.state-loading { color: #3b82f6; }
.state-error { background: #fef2f2; border-color: #fca5a5; color: #991b1b; }
.state-empty { color: #64748b; }
.error-msg { margin-bottom: 0.75rem; font-weight: 500; }
.btn-retry {
  padding: 0.45rem 1rem;
  background: #dc2626;
  color: white;
  border: none;
}
.btn-retry:hover { background: #b91c1c; }
.spinner {
  width: 28px;
  height: 28px;
  border: 3px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 0.75rem;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
