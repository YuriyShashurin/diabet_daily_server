from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.schemas import SugarIndicationRequestTelegram, SugarIndicationBase
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv
from api.views.get_postgres_db import get_postgres_db

router = APIRouter()


@cbv(router)
class IndicationCBV:
    db: Session = Depends(get_postgres_db)
    authorize: AuthJWT = Depends()

    @router.post('/')
    async def add_sugar_indication(self, data: SugarIndicationBase):
        self.authorize.jwt_required()
        current_user = self.authorize.get_jwt_subject()
        print(current_user,data.sugar_indication)


    @router.post('/telegram')
    async def add_sugar_indication_from_telegram(self, data: SugarIndicationRequestTelegram):
        pass
