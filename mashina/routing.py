from importlib.util import find_spec

from mashina.config import settings
from mashina.utils.misc import import_string

root_routes = []

for app in settings.APPS:
    if find_spec('%s.routes' % app):
        routes = import_string('%s.routes.routes' % app, silent=False)
        if routes is not None:
            root_routes.extend(routes)
