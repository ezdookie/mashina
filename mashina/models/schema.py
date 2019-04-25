from marshmallow_sqlalchemy import ModelSchema
from mashina.db import Session


class BaseSchema(ModelSchema):
    class Meta:
        sqla_session = Session
