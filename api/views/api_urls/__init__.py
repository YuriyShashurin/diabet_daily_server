from fastapi import APIRouter

from api.views.api_urls import indication_urls

api_router = APIRouter()
api_router.include_router(indication_urls.router, prefix='/sugar_indication')