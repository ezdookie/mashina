import json
import falcon
from mashina.utils.serialize import json_serializer


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

        # try:
        #     req.context['request'] = json.loads(body.decode('utf-8'))
        # except (ValueError, UnicodeDecodeError):
        #     raise falcon.HTTPError(
        #         falcon.HTTP_753,
        #         'Malformed JSON. Could not decode the request body.'
        #         'The JSON was incorrect or not encoded as UTF-8.'
        #     )

    def process_response(self, req, resp, resource, req_succeeded):
        if 'response' not in resp.context:
            return

        resp.body = json.dumps(
            resp.context['response'],
            default=json_serializer
        )
