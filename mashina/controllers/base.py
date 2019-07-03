import falcon


class APIBaseController(object):

    def __init__(self, Schema, *args, **kwargs):
        self.Schema = Schema
        self.query_params = {}
        self.objects_count = 0

    def get_schema(self, *args, **kwargs):
        return self.Schema(*args, **kwargs)

    def validate(self, data, partial=False, instance=None):
        schema = self.get_schema()
        marsh = schema.load(data, partial=partial, instance=instance)
        if marsh.errors:
            raise falcon.HTTPBadRequest('Validation error', marsh.errors)
        return marsh.data, schema

    def get_id_column(self):
        return '%s_id' % self.Schema.Meta.model.__table__.name.lower()
