from mashina.models.base import Base
from mashina.models.mixins import ModelGUIDMixin


class ${singular_capitalized}(ModelGUIDMixin, Base):
    __tablename__ = '${plural}'
