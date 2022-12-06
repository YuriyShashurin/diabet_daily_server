from typing import Any

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base: Any = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4)
    username = Column(String(50), unique=True)
    password = Column(String(50))
    email = Column(String(50), nullable=True)
    telegram_token = Column(UUID(as_uuid=True), index=True, unique=True, default=uuid.uuid4)
    is_authenticated = Column(Boolean, default=False)


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4)
    user_id = Column(
        UUID,
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False,
    )
    first_name = Column(String(30))
    last_name = Column(String(30))
    weight = Column(Float)
    birth = Column(Date)
    tg = Column(String(50), nullable=True)

    user = relationship('User', backref='profiles')
