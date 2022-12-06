from fastapi import APIRouter, Depends, HTTPException

from api.schemas import UserCreate, UserResponse, LoginUserBase, User
from project_config import app, SessionLocal, logger
from sqlalchemy.orm import Session
from api.utils import user_crud, user_validation

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


@app.post("/signup/", response_model=UserResponse, status_code=201)
async def signup(signup_data: UserCreate, db: Session = Depends(get_postgres_db)):
    new_user = await user_crud.user_register(signup_data, db)
    try:
        if new_user.id:
            return new_user
    except:
        if new_user[0] == 'Double':
            raise HTTPException(status_code=422, detail='Пользователь с указанными параметрами уже существует')
        else:
            logger.error(f'Ошибка регистрации {new_user[0]} {new_user[1]} {signup_data.username}')
            raise HTTPException(status_code=500, detail='Ошибка сервера, повторите позже')


@app.post("/login/", response_model=UserResponse, status_code=201)
async def login(login_data: LoginUserBase, db: Session = Depends(get_postgres_db)):
    user = await user_crud.login_user(login_data, db)
    try:
        if user.id:
            return user
    except:
        if not user:
            raise HTTPException(status_code=404, detail='Пользователь не найден')
        else:
            logger.error(f'Ошибка авторизации {user[0]} {user[1]} {login_data.username}')
            raise HTTPException(status_code=500, detail='Ошибка сервера, повторите позже')


# Обработка запроса на выход
@app.post('/logout/', response_model=UserResponse, status_code=201)
async def logout_user(id: User, db: Session = Depends(get_postgres_db)):
    user = await user_crud.logout_user(id, db)
    try:
        if user.id:
            return user
    except:
        if not user:
            raise HTTPException(status_code=404, detail='Пользователь не найден')
        else:
            logger.error(f'Ошибка разлогирования {user[0]} {user[1]} {id}')
            raise HTTPException(status_code=500, detail='Ошибка сервера, повторите позже')
