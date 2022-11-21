from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from project_config import config


if config.is_test:

    SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://{postgres_name}:{postgres_password}@{postgres_host}/{postgres_db}'.format(
        postgres_name=config.postgres_name_test,
        postgres_password=config.postgres_password_test,
        postgres_host=config.postgres_host_test,
        postgres_db=config.postgres_db_test
    )


else:
    SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://{postgres_name}:{postgres_password}@{postgres_host}/{postgres_db}'.format(
        postgres_name=config.postgres_name,
        postgres_password=config.postgres_password,
        postgres_host=config.postgres_host,
        postgres_db=config.postgres_db
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()