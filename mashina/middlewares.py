import json
import falcon
from mashina.db import Session
from mashina.utils.serialize import json_serializer


class Initializer(object):

    def process_resource(self, req, resp, resource, params):
        req.params['ordering'] = 'id'
        req.params['limit'] = 20 if 'limit' not in req.params else req.params['limit']
        req.params['offset'] = 0 if 'offset' not in req.params else req.params['offset']


class JSONTranslator(object):

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


class SQLAlchemySessionManager(object):

    def process_resource(self, req, resp, resource, params):
        # resource.session = Session()
        req.context['session'] = Session()

    def process_response(self, req, resp, resource, req_succeeded):
        if 'session' in req.context:
            if not req_succeeded:
                req.context['session'].rollback()
            Session.remove()
        # if hasattr(resource, 'session'):
        #     if not req_succeeded:
        #         resource.session.rollback()
        #     Session.remove()
