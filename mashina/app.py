import falcon

from mashina.config import settings
from mashina.routing import root_routes
from mashina.utils.misc import import_string


class App(falcon.API):
    def add_routes(self):
        for route in root_routes:
            self.add_route(*route)

    def get_middlewares(self):
        return [import_string(middleware)() for middleware in settings.MIDDLEWARE]

    def __init__(self):
        super(App, self).__init__(
            middleware=self.get_middlewares()
        )
        self.add_routes()
