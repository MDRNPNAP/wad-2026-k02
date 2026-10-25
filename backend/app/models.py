from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)  # 'admin' atau 'user'
    full_name = Column(String(100), nullable=False)

    sessions = relationship("TrainingSession", back_populates="owner", cascade="all, delete-orphan")

class TrainingSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    trainer = Column(String(60), nullable=False)
    department = Column(String(50), nullable=False)
    date = Column(String(10), nullable=False)
    duration_hours = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String(20), default="Scheduled")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    owner = relationship("User", back_populates="sessions")
