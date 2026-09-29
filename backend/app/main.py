from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.sessions import router as sessions_router

app = FastAPI(
    title="HR Training Sessions API",
    description="Backend API untuk Pencatat Sesi Pelatihan HR (Kelompok 1)",
    version="1.0.0"
)

# B5: Konfigurasi CORS hanya untuk origin frontend
FRONTEND_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint pemeriksaan kesehatan server."""
    return {"status": "ok"}

app.include_router(sessions_router)
