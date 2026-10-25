from sqlalchemy.orm import Session
from app.models import User, TrainingSession
from app.auth import hash_password
from app.data import sessions as initial_sessions

def seed_database(db: Session):
    """Seed data awal untuk database: admin user dan 12 data sesi HR."""
    # 1. Pastikan akun admin ada
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            full_name="Administrator HR",
            hashed_password=hash_password("admin123"),
            role="admin"
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

    # 2. Pastikan data awal sesi ada
    existing_count = db.query(TrainingSession).count()
    if existing_count == 0:
        for item in initial_sessions:
            session_obj = TrainingSession(
                title=item["title"],
                trainer=item["trainer"],
                department=item["department"],
                date=item["date"],
                duration_hours=item["duration_hours"],
                capacity=item["capacity"],
                status=item.get("status", "Scheduled"),
                owner_id=admin.id
            )
            db.add(session_obj)
        db.commit()
