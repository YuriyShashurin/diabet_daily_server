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
from api.views import auth_urls,api_urls

app.include_router(auth_urls.auth_router, prefix='/auth', tags=["auth"])
app.include_router(api_urls.api_router, prefix='/api/v1', tags=["api"])


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internet server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
