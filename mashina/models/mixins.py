import uuid
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID
from mashina.models.custom import GUID


class ModelIntegerIDMixin(object):
    id = Column(Integer, primary_key=True)


class ModelGUIDMixin(object):
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
