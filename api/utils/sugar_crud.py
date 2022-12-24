import datetime

from api.models import SugarIndication, User
from project_config import logger


async def sugar_indication_post(user_id, indication: float, db):
    try:
        new_indication = SugarIndication(user_id=user_id, sugar_indication=indication, date_time=datetime.datetime.now())
        db.add(new_indication)
        db.commit()
        return new_indication
    except Exception as e:
        logger.error(f'Adding sugar data for the user {user_id} failed with an error {e}')
        return None

async def check_telegram_id(telegram_id: int, db):
    try:
        user = db.query(User).filter(User.telegram_user_id == telegram_id).first()
        return user.id
    except Exception as e:
        logger.error(f'Adding sugar data for the telegram user {telegram_id} failed with an error {e}')
        return None
