from mashina.models.base import Base
from mashina.models.mixins import ModelGUIDMixin


class ${name}(ModelGUIDMixin, Base):
    __tablename__ = '${name_slug}'
