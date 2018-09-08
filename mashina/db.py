from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

engine = create_engine('postgresql://postgres@db:5432/postgres', echo=True)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
