from pydantic import BaseModel, Field
from typing import List, Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    role: str = Field(default="user", pattern="^(admin|user)$")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password minimal 6 karakter")

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class SessionBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    trainer: str = Field(..., min_length=3, max_length=60)
    department: str = Field(..., min_length=2, max_length=50)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    duration_hours: int = Field(..., gt=0, le=40)
    capacity: int = Field(..., gt=0, le=500)
    status: str = Field(default="Scheduled")

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    trainer: Optional[str] = Field(None, min_length=3, max_length=60)
    department: Optional[str] = Field(None, min_length=2, max_length=50)
    date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    duration_hours: Optional[int] = Field(None, gt=0, le=40)
    capacity: Optional[int] = Field(None, gt=0, le=500)
    status: Optional[str] = None

class SessionResponse(SessionBase):
    id: int
    owner_id: Optional[int] = None
    owner_name: Optional[str] = None

    class Config:
        from_attributes = True

class PaginatedSessionsResponse(BaseModel):
    items: List[SessionResponse]
    total: int
    page: int
    size: int
    total_pages: int
