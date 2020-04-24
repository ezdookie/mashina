from sqlalchemy.ext.declarative import declarative_base

from mashina.db import Session


class Base(object):
    @classmethod
    def objects(cls):
        return Session.query(cls)


BaseModel = declarative_base(cls=Base)
