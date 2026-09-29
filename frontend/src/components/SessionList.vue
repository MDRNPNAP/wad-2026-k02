<template>
  <div class="session-list-section">
    <div class="table-container">
      <table class="session-table" aria-label="Daftar Sesi Pelatihan">
        <thead>
          <tr>
            <th scope="col">Judul Pelatihan</th>
            <th scope="col">Pemateri</th>
            <th scope="col">Departemen</th>
            <th scope="col">Tanggal</th>
            <th scope="col">Kapasitas</th>
            <th scope="col">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in sessions" :key="s.id">
            <td class="font-medium">{{ s.title }}</td>
            <td>{{ s.trainer }}</td>
            <td>{{ s.department }}</td>
            <td>{{ s.date }}</td>
            <td>{{ s.capacity }} org ({{ s.duration_hours }}j)</td>
            <td>
              <button
                type="button"
                class="btn-delete"
                :aria-label="'Hapus sesi ' + s.title"
                @click="$emit('request-delete', s)"
              >
                Hapus
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <nav class="pagination-bar" aria-label="Navigasi Halaman">
      <span class="page-info">Halaman {{ page }} dari {{ totalPages }} (Total {{ total }} sesi)</span>
      <div class="page-btns">
        <button type="button" :disabled="page <= 1" @click="$emit('change-page', page - 1)">
          &larr; Sebelumnya
        </button>
        <button type="button" :disabled="page >= totalPages" @click="$emit('change-page', page + 1)">
          Selanjutnya &rarr;
        </button>
      </div>
    </nav>
  </div>
</template>

<script setup>
defineProps({
  sessions: { type: Array, required: true },
  page: { type: Number, required: true },
  totalPages: { type: Number, required: true },
  total: { type: Number, required: true }
})
defineEmits(['change-page', 'request-delete'])
</script>

<style scoped>
.table-container { overflow-x: auto; background: white; border-radius: 8px; border: 1px solid #e2e8f0; }
.session-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; }
th, td { padding: 0.75rem 1rem; border-bottom: 1px solid #e2e8f0; }
th { background: #f8fafc; font-weight: 600; color: #475569; }
.font-medium { font-weight: 500; color: #1e293b; }
.btn-delete { padding: 0.25rem 0.5rem; background: #fee2e2; color: #b91c1c; font-size: 0.8rem; }
.btn-delete:hover { background: #fecaca; }
.pagination-bar { display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; font-size: 0.875rem; flex-wrap: wrap; gap: 0.5rem; }
.page-btns { display: flex; gap: 0.5rem; }
.page-btns button { padding: 0.35rem 0.75rem; background: white; border: 1px solid #cbd5e1; }
.page-btns button:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
