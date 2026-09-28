import math
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Response, status
from app.data import sessions
from app.schemas import PaginatedSessionsResponse, SessionCreate, SessionResponse

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.get("", response_model=PaginatedSessionsResponse)
def get_sessions(
    page: int = Query(1, ge=1, description="Nomor halaman"),
    size: int = Query(5, ge=1, le=50, description="Jumlah data per halaman"),
    search: Optional[str] = Query(None, description="Kata kunci pencarian")
):
    """B1: Ambil daftar sesi dengan pagination dan filter pencarian."""
    filtered = sessions
    if search:
        term = search.strip().lower()
        filtered = [
            s for s in sessions
            if term in s["title"].lower()
            or term in s["trainer"].lower()
            or term in s["department"].lower()
        ]
    total = len(filtered)
    total_pages = max(1, math.ceil(total / size))
    start = (page - 1) * size
    items = filtered[start:start + size]
    return {"items": items, "total": total, "page": page, "size": size, "total_pages": total_pages}

@router.get("/{id}", response_model=SessionResponse)
def get_session_by_id(id: int):
    """B2: Ambil satu sesi berdasarkan ID, kembalikan 404 jika tidak ada."""
    for s in sessions:
        if s["id"] == id:
            return s
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sesi pelatihan tidak ditemukan")

@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(payload: SessionCreate):
    """B3: Buat sesi baru dengan validasi Pydantic terpisah, kembalikan 201."""
    next_id = max([s["id"] for s in sessions], default=0) + 1
    new_session = {"id": next_id, **payload.model_dump()}
    sessions.append(new_session)
    return new_session

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(id: int):
    """B4: Hapus sesi berdasarkan ID, kembalikan 204."""
    for index, s in enumerate(sessions):
        if s["id"] == id:
            sessions.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sesi pelatihan tidak ditemukan")
