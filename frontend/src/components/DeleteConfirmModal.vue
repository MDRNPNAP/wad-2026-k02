<template>
  <div v-if="session" class="modal-backdrop" @click.self="$emit('cancel')">
    <div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <h3 id="modal-title">Konfirmasi Penghapusan</h3>
      <p class="modal-desc">
        Apakah Anda yakin ingin menghapus sesi <strong>"{{ session.title }}"</strong>? Tindakan ini tidak dapat dibatalkan.
      </p>
      <div class="modal-actions">
        <button type="button" class="btn-cancel" @click="$emit('cancel')">Batal</button>
        <button type="button" class="btn-danger" :disabled="isDeleting" @click="$emit('confirm', session.id)">
          {{ isDeleting ? 'Menghapus...' : 'Ya, Hapus' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  session: { type: Object, default: null },
  isDeleting: { type: Boolean, default: false }
})
defineEmits(['confirm', 'cancel'])
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  display: grid;
  place-items: center;
  padding: 1rem;
  z-index: 50;
}
.modal-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  max-width: 420px;
  width: 100%;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}
.modal-desc { margin: 1rem 0 1.5rem; color: #475569; font-size: 0.95rem; }
.modal-actions { display: flex; justify-content: flex-end; gap: 0.75rem; }
.btn-cancel { padding: 0.5rem 1rem; background: #f1f5f9; color: #334155; }
.btn-cancel:hover { background: #e2e8f0; }
.btn-danger { padding: 0.5rem 1rem; background: #dc2626; color: white; }
.btn-danger:hover { background: #b91c1c; }
</style>
