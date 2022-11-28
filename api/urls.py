from fastapi import APIRouter

from project_config import app,SessionLocal

router = APIRouter()


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


