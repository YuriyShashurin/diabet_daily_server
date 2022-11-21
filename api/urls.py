from fastapi import APIRouter

from project_config import SessionLocal

router = APIRouter()


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()