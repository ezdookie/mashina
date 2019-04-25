class InitializerMiddleware(object):
    def process_resource(self, req, resp, resource, params):
        resource.req = req
        resource.resp = resp
