from fastapi import APIRouter, Depends

from api.schemas import SugarIndicationRequestTelegram
from sqlalchemy.orm import Session

from api.views.get_postgres_db import get_postgres_db

router = APIRouter()


@router.post('/')
async def add_sugar_indication(data: SugarIndicationRequestTelegram, db: Session = Depends(get_postgres_db)):
    pass
