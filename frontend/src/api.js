const API_BASE = 'http://localhost:8000/sessions'

export async function fetchSessions({ page = 1, size = 5, search = '', signal } = {}) {
  const url = new URL(API_BASE)
  url.searchParams.set('page', page)
  url.searchParams.set('size', size)
  if (search.trim()) url.searchParams.set('search', search.trim())

  const res = await fetch(url.toString(), { signal })
  if (!res.ok) throw new Error(`Gagal memuat data (HTTP ${res.status})`)
  return await res.json()
}

export async function createSessionApi(payload, { signal } = {}) {
  const res = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    signal
  })
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}))
    const msg = errorData.detail 
      ? (typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail))
      : `Gagal membuat sesi (HTTP ${res.status})`
    throw new Error(msg)
  }
  return await res.json()
}

export async function deleteSessionApi(id, { signal } = {}) {
  const res = await fetch(`${API_BASE}/${id}`, {
    method: 'DELETE',
    signal
  })
  if (!res.ok) throw new Error(`Gagal menghapus sesi (HTTP ${res.status})`)
  return true
}
