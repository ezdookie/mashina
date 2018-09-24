from falcon.routing import CompiledRouter, util
from mashina.constants import CONTROLLER_COLLECTION, CONTROLLER_RESOURCE

defined_methods = {
    CONTROLLER_COLLECTION: {
        'GET': 'on_get',
        'POST': 'on_post'
    },
    CONTROLLER_RESOURCE: {
        'GET': 'on_get_one',
        'PUT': 'on_put_one',
        'DELETE': 'on_delete_one',
    }
}


class MashinaRouter(CompiledRouter):

    def map_http_methods(self, resource, methods):
        method_map = {}
        _methods = {k: v for k, v in methods.items() if k not in resource.excluded_methods}

        for method_key, method_value in _methods.items():
            responder = getattr(resource, method_value)
            if callable(responder):
                method_map[method_key] = responder

        return method_map

    def add_route(self, uri_template, method_map, resource, *args):
        method_map = self.map_http_methods(resource, defined_methods[resource.controller_type])
        util.set_default_responders(method_map)
        super().add_route(uri_template, method_map, resource)
