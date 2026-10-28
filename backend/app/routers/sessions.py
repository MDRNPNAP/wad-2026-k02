import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models import TrainingSession, User
from app.schemas import PaginatedSessionsResponse, SessionCreate, SessionUpdate, SessionResponse
from app.auth import get_current_user, require_current_user

router = APIRouter(prefix="/sessions", tags=["Sessions"])

def format_session(s: TrainingSession) -> dict:
    return {
        "id": s.id, "title": s.title, "trainer": s.trainer,
        "department": s.department, "date": s.date,
        "duration_hours": s.duration_hours, "capacity": s.capacity,
        "status": s.status, "owner_id": s.owner_id,
        "owner_name": s.owner.full_name if s.owner else "System"
    }

@router.get("", response_model=PaginatedSessionsResponse)
def get_sessions(
    page: int = Query(1, ge=1),
    size: int = Query(5, ge=1, le=50),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(TrainingSession)
    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(or_(
            TrainingSession.title.ilike(term),
            TrainingSession.trainer.ilike(term),
            TrainingSession.department.ilike(term)
        ))
    total = query.count()
    total_pages = max(1, math.ceil(total / size))
    records = query.order_by(TrainingSession.id.desc()).offset((page - 1) * size).limit(size).all()
    return {"items": [format_session(r) for r in records], "total": total, "page": page, "size": size, "total_pages": total_pages}

@router.get("/{id}", response_model=SessionResponse)
def get_session_by_id(id: int, db: Session = Depends(get_db)):
    s = db.query(TrainingSession).filter(TrainingSession.id == id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sesi pelatihan tidak ditemukan")
    return format_session(s)

@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(payload: SessionCreate, current_user: User = Depends(require_current_user), db: Session = Depends(get_db)):
    new_s = TrainingSession(**payload.model_dump(), owner_id=current_user.id)
    db.add(new_s)
    db.commit()
    db.refresh(new_s)
    return format_session(new_s)

@router.put("/{id}", response_model=SessionResponse)
def update_session(id: int, payload: SessionUpdate, current_user: User = Depends(require_current_user), db: Session = Depends(get_db)):
    s = db.query(TrainingSession).filter(TrainingSession.id == id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sesi pelatihan tidak ditemukan")
    if s.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Akses ditolak: Anda tidak memiliki izin untuk mengubah data milik pengguna lain.")
    for key, val in payload.model_dump(exclude_unset=True).items():
        if val is not None:
            setattr(s, key, val)
    db.commit()
    db.refresh(s)
    return format_session(s)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(id: int, current_user: User = Depends(require_current_user), db: Session = Depends(get_db)):
    s = db.query(TrainingSession).filter(TrainingSession.id == id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sesi pelatihan tidak ditemukan")
    if s.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Akses ditolak: Anda tidak memiliki izin untuk menghapus data milik pengguna lain.")
    db.delete(s)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
