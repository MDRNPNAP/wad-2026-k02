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
    <button type="button" class="btn-create" @click="$emit('open-create')">
      + Tambah Sesi
    </button>
  </section>
</template>

<script setup>
defineProps({ modelValue: { type: String, default: '' } })
defineEmits(['update:modelValue', 'open-create'])
</script>

<style scoped>
.toolbar { display: flex; justify-content: space-between; align-items: flex-end; gap: 1rem; margin-bottom: 1.25rem; flex-wrap: wrap; }
.search-wrap { flex: 1; min-width: 240px; display: flex; flex-direction: column; gap: 0.25rem; }
.search-wrap label { font-size: 0.85rem; font-weight: 600; color: #475569; }
.btn-create { padding: 0.6rem 1.2rem; background: #2563eb; color: white; border: none; font-size: 0.9rem; }
.btn-create:hover { background: #1d4ed8; }
</style>
