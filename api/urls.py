from fastapi import APIRouter

from project_config import app,SessionLocal

router = APIRouter()


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/signup")
def signup():
    return {"Hello": "World"}


@app.post("/login")
def login():
    return {"Hello": "World"}
