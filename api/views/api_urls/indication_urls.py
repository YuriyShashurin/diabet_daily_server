import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException, MissingTokenError
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.schemas import SugarIndicationRequestTelegram, SugarIndicationBase, SugarIndicationResponseSite
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv

from api.utils.sugar_crud import sugar_indication_post
from api.views.get_postgres_db import get_postgres_db
from project_config import logger
from api.utils import sugar_crud

router = APIRouter()


@cbv(router)
class IndicationCBV:
    db: Session = Depends(get_postgres_db)
    authorize: AuthJWT = Depends()

    @router.post('/', response_model=SugarIndicationResponseSite)
    async def add_sugar_indication(self, data: SugarIndicationBase):
        try:
            self.authorize.jwt_required()
            user_id = self.authorize.get_raw_jwt()['id']
            new_indication = await sugar_crud.sugar_indication_post(user_id, data.sugar_indication, self.db)
            print(type(new_indication), new_indication)

            if new_indication is not None:
                return new_indication
            else:
                raise HTTPException(status_code=422, detail=f'Adding sugar data for the user {user_id} failed with an error')
        except MissingTokenError:
            logger.error(f'JWT token for the user {user_id} miss')
            raise HTTPException(status_code=401, detail="Missing Authorization Header")
        except Exception as e:
            logger.error(f'Error for user {user_id} - {e.detail}')
            raise HTTPException(status_code=500, detail=e.detail)

    @router.post('/telegram', response_model=SugarIndicationResponseSite)
    async def add_sugar_indication_from_telegram(self, data: SugarIndicationRequestTelegram):
        try:
            user_id = await sugar_crud.check_telegram_id(data.telegram_id, self.db)

            if user_id is not None:
                new_indication = await sugar_crud.sugar_indication_post(str(user_id),data.sugar_indication, self.db)
                if new_indication is not None:
                    return new_indication
                else:
                    raise HTTPException(status_code=422, detail=f'Adding sugar data for the user {user_id} failed with an error')
            else:
                pass
        except Exception as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)





