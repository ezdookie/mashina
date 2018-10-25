from apps.${plural}.controllers import ${singular_capitalized}APIController
from mashina.constants import CONTROLLER_COLLECTION, CONTROLLER_RESOURCE

routes = [
    ('/${plural}/', ${singular_capitalized}APIController(CONTROLLER_COLLECTION)),
    ('/${plural}/{${singular}_id:uuid}', ${singular_capitalized}APIController(CONTROLLER_RESOURCE)),
]
