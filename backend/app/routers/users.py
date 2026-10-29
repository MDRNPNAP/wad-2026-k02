from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.auth import hash_password, require_admin

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Hanya Admin yang dapat membuat akun baru (User A, User B)."""
    username_clean = payload.username.strip().lower()
    existing = db.query(User).filter(User.username == username_clean).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username sudah digunakan"
        )
    
    new_user = User(
        username=username_clean,
        full_name=payload.full_name.strip(),
        hashed_password=hash_password(payload.password),
        role=payload.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("", response_model=List[UserResponse])
def get_all_users(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Melihat daftar seluruh pengguna (khusus admin)."""
    return db.query(User).all()
