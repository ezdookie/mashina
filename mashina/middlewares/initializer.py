class InitializerMiddleware(object):
    def process_resource(self, req, resp, resource, params):
        req.params['ordering'] = 'id'
        req.params['limit'] = 20 if 'limit' not in req.params else req.params['limit']
        req.params['offset'] = 0 if 'offset' not in req.params else req.params['offset']
        req.context['exact_filters'] = {}
