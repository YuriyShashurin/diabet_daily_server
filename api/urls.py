from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse

from api.schemas import UserCreate, UserToken, UserLogout, LoginUserBase, User, JWTSettings
from project_config import app, SessionLocal, logger
from sqlalchemy.orm import Session
from api.utils import user_crud, user_validation

router = APIRouter()


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return JWTSettings()


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    user_id = Authorize.get_raw_jwt()['id']
    expires = timedelta(days=2)
    another_claims = {"id": user_id}
    new_access_token = Authorize.create_access_token(subject=current_user,
                                                     expires_time=expires,
                                                     user_claims=another_claims)
    return {"access_token": new_access_token}


@app.post("/signup/", response_model=User, status_code=201)
async def signup(signup_data: UserCreate, db: Session = Depends(get_postgres_db)):
    new_user = await user_crud.user_register(signup_data, db)
    try:
        if new_user.id:
            print(new_user.id, new_user.is_authenticated)
            return new_user
    except:
        if new_user[0] == 'Double':
            raise HTTPException(status_code=422, detail='Пользователь с указанными параметрами уже существует')
        else:
            logger.error(f'Ошибка регистрации {new_user[0]} {new_user[1]} {signup_data.username}')
            raise HTTPException(status_code=500, detail='Ошибка сервера, повторите позже')


@app.post("/login/", response_model=UserToken, status_code=201)
async def login(login_data: LoginUserBase, db: Session = Depends(get_postgres_db), Authorize: AuthJWT = Depends()):
    user = await user_crud.login_user(login_data, db)
    try:
        if user.id:
            expires = timedelta(days=1)
            another_claims = {"id": str(user.id)}
            print(another_claims)
            access_token = Authorize.create_access_token(subject=user.username,
                                                         expires_time=expires,
                                                         user_claims=another_claims)
            refresh_token = Authorize.create_refresh_token(subject=user.username)
            print(access_token)
            result = {'id': user.id,
                      'is_authenticated': user.is_authenticated,
                      "access_token": access_token,
                      "refresh_token": refresh_token,
                      }

            print(result)
            return result
    except Exception as e:
        if user is None:
            raise HTTPException(status_code=401, detail='Bad username or password')
        # TODO: поменять обработку событий
        else:
            print(e)
            raise HTTPException(status_code=e.status_code, detail=e.message)


# Обработка запроса на выход

@app.post('/logout/', response_model=UserLogout, status_code=201)
async def logout_user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_postgres_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await user_crud.logout_user(current_user, db)
    try:
        if user.id:
            return user
    except:
        if not user:
            raise HTTPException(status_code=401, detail='Пользователь не найден')
        else:
            logger.error(f'Ошибка разлогирования {user[0]} {user[1]} {id}')
            raise HTTPException(status_code=500, detail='Ошибка сервера, повторите позже')
