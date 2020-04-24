from sqlalchemy import Column, String

from mashina.models import BaseModel
from mashina.models.mixins import ModelGUIDMixin, ModelTimestampMixin


class {{ singular_capitalized }}Model(ModelTimestampMixin, ModelGUIDMixin, BaseModel):
    __tablename__ = '{{ singular }}'

    name = Column(String(255), nullable=False)
