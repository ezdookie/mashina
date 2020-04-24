from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from mashina.config import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
