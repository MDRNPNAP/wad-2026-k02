<template>
  <div class="container">
    <header class="app-header">
      <h1>Pencatat Sesi Pelatihan HR</h1>
      <p class="subtitle">Kelompok 1 &middot; Human Resources Internal Training</p>
    </header>

    <main>
      <AppToolbar v-model="searchQuery" @update:model-value="onSearch" @open-create="isFormOpen = true" />
      <StateFeedback :state="state" :error-message="errorMsg" @retry="loadData" />
      <SessionList
        v-if="state === 'data'"
        :sessions="items" :page="page" :total-pages="totalPages" :total="total"
        @change-page="(p) => { page = p; loadData() }"
        @request-delete="targetDelete = $event"
      />
    </main>

    <SessionFormModal
      :is-open="isFormOpen" :is-submitting="isSubmitting" :server-error="formError"
      @close="isFormOpen = false" @submit="handleCreate"
    />
    <DeleteConfirmModal
      :session="targetDelete" :is-deleting="isDeleting"
      @cancel="targetDelete = null" @confirm="handleDelete"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { fetchSessions, createSessionApi, deleteSessionApi } from './api.js'
import AppToolbar from './components/AppToolbar.vue'
import StateFeedback from './components/StateFeedback.vue'
import SessionList from './components/SessionList.vue'
import SessionFormModal from './components/SessionFormModal.vue'
import DeleteConfirmModal from './components/DeleteConfirmModal.vue'

const items = ref([]), state = ref('loading'), errorMsg = ref('')
const page = ref(1), totalPages = ref(1), total = ref(0), searchQuery = ref('')
const isFormOpen = ref(false), isSubmitting = ref(false), formError = ref('')
const targetDelete = ref(null), isDeleting = ref(false)
let controller = null, searchTimer = null

async function loadData() {
  controller?.abort(); controller = new AbortController()
  state.value = 'loading'; errorMsg.value = ''
  try {
    const res = await fetchSessions({ page: page.value, size: 5, search: searchQuery.value, signal: controller.signal })
    items.value = res.items; total.value = res.total; totalPages.value = res.total_pages
    state.value = res.items.length === 0 ? 'empty' : 'data'
  } catch (err) {
    if (err.name === 'AbortError') return
    state.value = 'error'; errorMsg.value = err.message || 'Gagal terhubung ke server backend'
  }
}

function onSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadData() }, 300)
}

async function handleCreate(payload) {
  isSubmitting.value = true; formError.value = ''
  try {
    await createSessionApi(payload)
    isFormOpen.value = false; await loadData()
  } catch (err) { formError.value = err.message }
  finally { isSubmitting.value = false }
}

async function handleDelete(id) {
  isDeleting.value = true
  try {
    await deleteSessionApi(id)
    targetDelete.value = null; await loadData()
  } catch (err) { alert(err.message) }
  finally { isDeleting.value = false }
}

onMounted(loadData)
onUnmounted(() => { controller?.abort(); clearTimeout(searchTimer) })
</script>

<style scoped>
.app-header { margin: 1rem 0 1.5rem; text-align: center; }
.subtitle { color: #64748b; font-size: 0.95rem; margin-top: 0.25rem; }
</style>
