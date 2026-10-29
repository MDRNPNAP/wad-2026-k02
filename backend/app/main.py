from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.seed import seed_database
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.sessions import router as sessions_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Buat tabel dan seed data awal jika belum ada
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title="HR Training Sessions API",
    description="Backend API untuk Pencatat Sesi Pelatihan HR dengan Database SQLite, Auth & RBAC",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(sessions_router)
