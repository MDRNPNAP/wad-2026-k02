<template>
  <section class="toolbar" aria-label="Aksi dan Pencarian">
    <div class="search-wrap">
      <label for="search-input">Pencarian Sesi</label>
      <input
        id="search-input"
        :value="modelValue"
        type="search"
        placeholder="Cari judul, pemateri, departemen..."
        @input="$emit('update:modelValue', $event.target.value)"
      />
    </div>
    <div class="btn-group">
      <button v-if="currentUser?.role === 'admin'" type="button" class="btn-admin" @click="$emit('open-admin')">
        ⚙️ Buat Akun (Admin)
      </button>
      <button v-if="currentUser" type="button" class="btn-create" @click="$emit('open-create')">
        + Tambah Sesi
      </button>
      <button v-if="!currentUser" type="button" class="btn-login" @click="$emit('open-login')">
        Login
      </button>
      <button v-else type="button" class="btn-logout" @click="$emit('logout')">
        Logout ({{ currentUser.username }})
      </button>
    </div>
  </section>
</template>

<script setup>
defineProps({
  modelValue: { type: String, default: '' },
  currentUser: { type: Object, default: null }
})
defineEmits(['update:modelValue', 'open-create', 'open-login', 'logout', 'open-admin'])
</script>

<style scoped>
.toolbar { display: flex; justify-content: space-between; align-items: flex-end; gap: 1rem; margin-bottom: 1.25rem; flex-wrap: wrap; }
.search-wrap { flex: 1; min-width: 240px; display: flex; flex-direction: column; gap: 0.25rem; }
.search-wrap label { font-size: 0.85rem; font-weight: 600; color: #475569; }
.btn-group { display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; }
.btn-create { padding: 0.55rem 1rem; background: #2563eb; color: white; border: none; border-radius: 6px; font-size: 0.875rem; cursor: pointer; }
.btn-create:hover { background: #1d4ed8; }
.btn-admin { padding: 0.55rem 1rem; background: #4f46e5; color: white; border: none; border-radius: 6px; font-size: 0.875rem; cursor: pointer; }
.btn-admin:hover { background: #4338ca; }
.btn-login { padding: 0.55rem 1rem; background: #0f172a; color: white; border: none; border-radius: 6px; font-size: 0.875rem; cursor: pointer; }
.btn-logout { padding: 0.55rem 0.85rem; background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.875rem; cursor: pointer; }
</style>
