from mashina.db import Session


class SQLAlchemySessionMiddleware(object):
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
