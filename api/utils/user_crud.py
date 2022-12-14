from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.models import User
from api.schemas import LoginUserBase
from project_config import logger


async def user_register(data, db):
    try:
        new_user = User(**data.dict())
        new_user.is_authenticated = True
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f'The User {new_user.id} added')
        return new_user
    except IntegrityError as err:
        print(err.args)
        return ['Double', err]
    except Exception as err:
        return ['Error', err]


async def login_user(data: LoginUserBase, db: Session):
    try:
        db_user = db.query(User).get(User.username == data.username and User.password == data.password)
        if db_user:
            db_user.is_authenticated = True
            db.commit()
            db.refresh(db_user)
            logger.info(f'The User @{data.username} logged in')
            return db_user
        else:
            return None
    except Exception as err:
        return ['Error', err]


async def logout_user(username, db: Session):
    try:
        db_user = db.query(User).get(User.username == username)
        if db_user:
            db_user.is_authenticated = False
            db.commit()
            db.refresh(db_user)
            logger.info(f'The User {id} logged out')
            return db_user
        else:
            return None
    except Exception as err:
        return ['Error', err]
