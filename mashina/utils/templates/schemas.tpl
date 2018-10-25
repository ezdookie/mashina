from marshmallow_sqlalchemy import ModelSchema
from apps.${plural}.models import ${singular_capitalized}


class ${singular_capitalized}Schema(ModelSchema):
    class Meta:
        model = ${singular_capitalized}
