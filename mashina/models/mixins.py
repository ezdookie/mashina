from sqlalchemy import Column, Integer


class ModelIntegerIDMixin(object):

    id = Column(Integer, primary_key=True)
