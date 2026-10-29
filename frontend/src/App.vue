<template>
  <div class="container">
    <LoginForm
      v-if="!currentUser && !isGuestMode"
      @login-success="onLoginSuccess"
      @guest-mode="onGuestMode"
    />

    <template v-else>
      <header class="app-header">
        <h1>Pencatat Sesi Pelatihan HR</h1>
        <p class="subtitle">Kelompok 1 &middot; SQLite Persistence &middot; RBAC Auth</p>
      </header>

      <main>
        <AppToolbar
          v-model="searchQuery" :current-user="currentUser"
          @update:model-value="onSearch" @open-create="isFormOpen = true"
          @open-login="isGuestMode = false" @open-admin="isAdminOpen = true"
          @logout="handleLogout"
        />
        <StateFeedback :state="state" :error-message="errorMsg" @retry="loadData" />
        <SessionList
          v-if="state === 'data'"
          :sessions="items" :page="page" :total-pages="totalPages" :total="total"
          @change-page="(p) => { page = p; loadData() }"
          @request-edit="openEdit" @request-delete="targetDelete = $event"
        />
      </main>

      <AdminUserModal :is-open="isAdminOpen" @close="isAdminOpen = false" />
      <SessionFormModal :is-open="isFormOpen" :is-submitting="isSubmitting" :server-error="formError" @close="isFormOpen = false" @submit="handleCreate" />
      <SessionEditModal :is-open="isEditOpen" :session="targetEdit" :is-submitting="isEditing" :server-error="editError" @close="isEditOpen = false" @submit="handleUpdate" />
      <DeleteConfirmModal :session="targetDelete" :is-deleting="isDeleting" @cancel="targetDelete = null" @confirm="handleDelete" />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { fetchSessions, createSessionApi, updateSessionApi, deleteSessionApi, getStoredUser, clearAuth } from './api.js'
import AppToolbar from './components/AppToolbar.vue'
import StateFeedback from './components/StateFeedback.vue'
import SessionList from './components/SessionList.vue'
import SessionFormModal from './components/SessionFormModal.vue'
import SessionEditModal from './components/SessionEditModal.vue'
import DeleteConfirmModal from './components/DeleteConfirmModal.vue'
import LoginForm from './components/LoginForm.vue'
import AdminUserModal from './components/AdminUserModal.vue'

const items = ref([]), state = ref('loading'), errorMsg = ref(''), page = ref(1), totalPages = ref(1), total = ref(0), searchQuery = ref('')
const isFormOpen = ref(false), isSubmitting = ref(false), formError = ref('')
const isEditOpen = ref(false), targetEdit = ref(null), isEditing = ref(false), editError = ref('')
const targetDelete = ref(null), isDeleting = ref(false)
const isAdminOpen = ref(false), currentUser = ref(getStoredUser()), isGuestMode = ref(false)
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
    state.value = 'error'; errorMsg.value = err.message || 'Gagal terhubung ke backend'
  }
}

function onSearch() { clearTimeout(searchTimer); searchTimer = setTimeout(() => { page.value = 1; loadData() }, 300) }
function onLoginSuccess(u) { currentUser.value = u; isGuestMode.value = false; loadData() }
function onGuestMode() { isGuestMode.value = true; loadData() }
function handleLogout() { clearAuth(); currentUser.value = null; isGuestMode.value = false }
function openEdit(s) { targetEdit.value = s; editError.value = ''; isEditOpen.value = true }

async function handleCreate(payload) {
  isSubmitting.value = true; formError.value = ''
  try { await createSessionApi(payload); isFormOpen.value = false; await loadData() }
  catch (err) { formError.value = err.message } finally { isSubmitting.value = false }
}

async function handleUpdate(payload) {
  isEditing.value = true; editError.value = ''
  try { await updateSessionApi(targetEdit.value.id, payload); isEditOpen.value = false; await loadData() }
  catch (err) { editError.value = err.message } finally { isEditing.value = false }
}

async function handleDelete(id) {
  isDeleting.value = true
  try { await deleteSessionApi(id); targetDelete.value = null; await loadData() }
  catch (err) { alert(err.message) } finally { isDeleting.value = false }
}

onMounted(() => { if (currentUser.value || isGuestMode.value) loadData() })
onUnmounted(() => { controller?.abort(); clearTimeout(searchTimer) })
</script>

<style scoped>
.app-header { margin: 1rem 0 1.5rem; text-align: center; }
.subtitle { color: #64748b; font-size: 0.95rem; margin-top: 0.25rem; }
</style>
