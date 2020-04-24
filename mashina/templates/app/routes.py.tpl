from {{ app_package }}.schemas import {{ singular_capitalized }}Schema

from mashina.controllers.generics import APIListCreateController, APIRetrieveUpdateDestroyController

routes = [
    ('/{{ plural }}', APIListCreateController({{ singular_capitalized }}Schema)),
    ('/{{ plural }}/{{ '{' }}{{ singular }}_id}', APIRetrieveUpdateDestroyController({{ singular_capitalized }}Schema))
]
