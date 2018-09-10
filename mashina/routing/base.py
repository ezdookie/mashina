from importlib import import_module
from config import settings

root_routes = []

for app in settings.APPS:
    app_routes_module = import_module('%s.routes' % app)
    root_routes.extend(getattr(app_routes_module, 'routes'))
