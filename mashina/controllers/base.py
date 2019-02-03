from mashina.controllers.mixins import APICollectionGETMixin, APICollectionPOSTMixin, \
    APIResourceControllerMixin


class APIBaseController(object):

    def __init__(self, controller_type, exclude=None, *args, **kwargs):
        self.controller_type = controller_type
        self.excluded_methods = exclude or []
        self.model = self.Schema.Meta.model

    def initialize(self, req, resp, **kwargs):
        self.req = req
        self.resp = resp
        if kwargs:
            self.req.context['request'].update(kwargs)

    @property
    def Schema(self):
        raise NotImplementedError


class APIController(APICollectionGETMixin, APICollectionPOSTMixin, \
        APIResourceControllerMixin, APIBaseController):

    def on_post(self, req, resp, **kwargs):
        self.initialize(req, resp, **kwargs)
        resp.context['response'] = self.get_post_response(**kwargs)

    def on_get_one(self, req, resp, **kwargs):
        self.initialize(req, resp, **kwargs)
        resp.context['response'] = self.get_one_response(**kwargs)

    def on_put_one(self, req, resp, **kwargs):
        self.initialize(req, resp, **kwargs)
        print ('on_put_one')

    def on_delete_one(self, req, resp, **kwargs):
        self.initialize(req, resp, **kwargs)
        print ('on_delete_one')
