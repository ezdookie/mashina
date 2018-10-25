from apps.${name_slug}.controllers import ${name}APIController
from mashina.constants import CONTROLLER_COLLECTION, CONTROLLER_RESOURCE

routes = [
    ('/${name_slug}/', ${name}APIController(CONTROLLER_COLLECTION)),
    ('/${name_slug}/{${name_slug}_id:uuid}', ${name}APIController(CONTROLLER_RESOURCE)),
]
