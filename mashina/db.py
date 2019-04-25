from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import settings


str_conn = 'postgresql://{user}:{password}@{host}:{port}/{db_name}'.format(
    user=settings.DATABASE['db_user'],
    password=settings.DATABASE['db_password'],
    host=settings.DATABASE['db_host'],
    port=settings.DATABASE['db_port'],
    db_name=settings.DATABASE['db_name']
)

engine = create_engine(str_conn, echo=settings.DEBUG)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
