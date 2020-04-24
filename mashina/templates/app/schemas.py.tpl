from {{ app_package }}.models import {{ singular_capitalized }}Model

from mashina.schemas import BaseSchema


class {{ singular_capitalized }}Schema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = {{ singular_capitalized }}Model
