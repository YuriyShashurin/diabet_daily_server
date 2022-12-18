from project_config import SessionLocal


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
