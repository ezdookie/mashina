from marshmallow_sqlalchemy import ModelSchema
from apps.${name_slug}.models import ${name}


class ${name}Schema(ModelSchema):
    class Meta:
        model = ${name}
