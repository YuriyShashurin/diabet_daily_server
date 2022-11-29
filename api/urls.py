from fastapi import APIRouter, Depends

from api.schemas import UserCreate, UserResponse
from project_config import app, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/app/")
def read_root():
    return {"Hello": "World"}


@app.post("/signup/", response_model=UserResponse)
def signup(signup_data: UserCreate, db: Session = Depends(get_postgres_db)):
    return signup_data


@app.post("/login/")
def login():
    return {"Hello": "World"}
