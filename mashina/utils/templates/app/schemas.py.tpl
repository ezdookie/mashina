from mashina.models.schema import BaseSchema
from {{ package }}.{{ plural }}.models import {{ singular_capitalized }}Model


class {{ singular_capitalized }}Schema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = {{ singular_capitalized }}Model
