import logging
from logging.config import dictConfig

from fastapi import FastAPI
from project_config import settings

from project_config.logs_config import LogConfig

config = settings.ConfigSettings()

app = FastAPI()

dictConfig(LogConfig().dict())
logger = logging.getLogger("diabet_daily")

from starlette.requests import Request
from starlette.responses import Response
from project_config.db import SessionLocal
from api import urls
from api import models

app.include_router(urls.router, prefix='/api/v1', tags=["api"])


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internet server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
