import falcon
from config import settings
from mashina.routing.base import root_routes
from mashina.utils.misc import import_string


class App(falcon.API):

    def add_routes(self):
        for route in root_routes:
            self.add_route(*route)

    def get_middlewares(self):
        return [import_string(middleware)() for middleware in settings.MIDDLEWARE]

    def __init__(self):
        super().__init__(
            middleware=self.get_middlewares()
        )
        self.add_routes()
