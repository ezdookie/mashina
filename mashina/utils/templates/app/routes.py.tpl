from mashina.controllers.api import APIListCreateController, APIRetrieveController
from {{ package }}.{{ plural }}.schemas import {{ singular_capitalized }}Schema

routes = [
    ('/{{ plural }}', APIListCreateController({{ singular_capitalized }}Schema)),
    ('/{{ plural }}/{{ '{' }}{{ singular }}_id}', APIRetrieveController({{ singular_capitalized }}Schema))
]
