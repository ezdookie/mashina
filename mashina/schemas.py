import falcon
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemyAutoSchemaOpts

from mashina.db import Session


class BaseOpts(SQLAlchemyAutoSchemaOpts):
    def __init__(self, meta, ordered=False):
        if not hasattr(meta, 'sqla_session'):
            meta.sqla_session = Session
        meta.load_instance = True
        meta.include_fk = True
        super(BaseOpts, self).__init__(meta, ordered=ordered)


class BaseSchema(SQLAlchemyAutoSchema):
    OPTIONS_CLASS = BaseOpts

    def save(self, data):
        self.session.add(data)
        self.session.commit()

    def handle_error(self, exc, *args, **kwargs):
        raise falcon.HTTPBadRequest(description=exc.messages)
