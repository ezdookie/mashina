from mashina.models.base import Base
from mashina.models.mixins import ModelGUIDMixin
from sqlalchemy import Column


class {{ singular_capitalized }}Model(ModelGUIDMixin, Base):
    __tablename__ = '{{ singular }}'
