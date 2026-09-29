from pydantic import BaseModel, Field
from typing import List, Optional

class SessionBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Judul sesi pelatihan")
    trainer: str = Field(..., min_length=3, max_length=60, description="Nama pemateri")
    department: str = Field(..., min_length=2, max_length=50, description="Departemen target")
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Tanggal pelaksanaan (YYYY-MM-DD)")
    duration_hours: int = Field(..., gt=0, le=40, description="Durasi dalam jam")
    capacity: int = Field(..., gt=0, le=500, description="Kapasitas maksimum peserta")
    status: str = Field(default="Scheduled", description="Status sesi (Scheduled, Completed, Cancelled)")

class SessionCreate(SessionBase):
    """Skema input untuk membuat sesi baru (tanpa id)."""
    pass

class SessionResponse(SessionBase):
    """Skema output yang dikembalikan ke klien (dilengkapi id)."""
    id: int

    class Config:
        from_attributes = True

class PaginatedSessionsResponse(BaseModel):
    """Skema output berpaginasi untuk daftar sesi pelatihan."""
    items: List[SessionResponse]
    total: int
    page: int
    size: int
    total_pages: int
