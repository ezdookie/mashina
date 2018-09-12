from mashina.utils.misc import import_string
from config import settings

root_routes = []

for app in settings.APPS:
    routes = import_string('%s.routes.routes' % app, silent=True)
    if routes is not None:
        root_routes.extend(routes)
