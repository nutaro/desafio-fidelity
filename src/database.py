from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from config import Config


def get_engine() -> Engine:
    driver = Config.DATABASE_DRIVER
    user = Config.DATABASE_USER
    password = Config.DATABASE_PASSWORD
    host = Config.DATABASE_HOST
    port = Config.DATABASE_PORT
    database = Config.DATABASE_NAME
    return create_engine(f'{driver}://{user}:{password}@{host}:{port}/{database}', echo=True)


def get_session() -> Session:
    return sessionmaker(bind=get_engine(), autocommit=False, autoflush=False, expire_on_commit=False)()
