import json
from uuid import UUID

import falcon


class JSONTranslatorMiddleware(object):
    def process_resource(self, req, resp, resource, params):
        if req.method in ['POST', 'PUT', 'PATCH']:
            body = req.stream.read(req.content_length or 0)
            if not body:
                raise falcon.HTTPBadRequest(
                    'Empty request body',
                    'A valid JSON document is required.'
                )
            req.context['request'] = json.loads(body)

    def process_response(self, req, resp, resource, req_succeeded):
        if req_succeeded:
            resp.body = json.dumps(resp.context.get('response'), cls=UUIDEncoder)


class UUIDEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        return json.JSONEncoder.default(self, o)
