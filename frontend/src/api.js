const BASE_URL = 'http://localhost:8000'

export function getToken() {
  return localStorage.getItem('token') || ''
}

export function setAuth(token, user) {
  localStorage.setItem('token', token)
  localStorage.setItem('user', JSON.stringify(user))
}

export function clearAuth() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

export function getStoredUser() {
  try {
    const raw = localStorage.getItem('user')
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

function authHeaders() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export async function loginApi(username, password) {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Login gagal')
  }
  const data = await res.json()
  setAuth(data.access_token, data.user)
  return data
}

export async function createUserApi(payload) {
  const res = await fetch(`${BASE_URL}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(payload)
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Gagal membuat akun (HTTP ${res.status})`)
  }
  return await res.json()
}

export async function fetchSessions({ page = 1, size = 5, search = '', signal } = {}) {
  const url = new URL(`${BASE_URL}/sessions`)
  url.searchParams.set('page', page)
  url.searchParams.set('size', size)
  if (search.trim()) url.searchParams.set('search', search.trim())

  const res = await fetch(url.toString(), { headers: authHeaders(), signal })
  if (!res.ok) throw new Error(`Gagal memuat data (HTTP ${res.status})`)
  return await res.json()
}

export async function createSessionApi(payload, { signal } = {}) {
  const res = await fetch(`${BASE_URL}/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(payload),
    signal
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Gagal membuat sesi (HTTP ${res.status})`)
  }
  return await res.json()
}

export async function updateSessionApi(id, payload, { signal } = {}) {
  const res = await fetch(`${BASE_URL}/sessions/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(payload),
    signal
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Gagal mengupdate sesi (HTTP ${res.status})`)
  }
  return await res.json()
}

export async function deleteSessionApi(id, { signal } = {}) {
  const res = await fetch(`${BASE_URL}/sessions/${id}`, {
    method: 'DELETE',
    headers: authHeaders(),
    signal
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Gagal menghapus sesi (HTTP ${res.status})`)
  }
  return true
}
