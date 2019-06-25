import uuid
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from mashina.models.custom import GUID


class ModelIntegerIDMixin(object):
    id = Column(Integer, primary_key=True)


class ModelGUIDMixin(object):
    id = Column(GUID, primary_key=True, default=uuid.uuid4)


class ModelTimestampMixin(object):
    @declared_attr
    def created_at(self):
        return Column(DateTime, server_default=func.now())

    @declared_attr
    def updated_at(self):
        return Column(DateTime, onupdate=func.now())
