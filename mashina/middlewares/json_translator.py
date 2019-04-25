import json
import falcon


class JSONTranslatorMiddleware(object):

    def process_resource(self, req, resp, resource, params):
        req.context['request'] = {}
        if req.content_length in (None, 0):
            return
        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest(
                'Empty request body. A valid JSON document is required.'
            )
        req.context['request'] = json.loads(body)

    def process_response(self, req, resp, resource, req_succeeded):
        resp.body = json.dumps(resp.context.get('response'))
