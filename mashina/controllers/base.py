from mashina.controllers.mixins import APICollectionControllerMixin, APIResourceControllerMixin


class APIBaseController(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = self.schema.Meta.model

    @property
    def schema(self):
        raise NotImplementedError


class APIController(APICollectionControllerMixin, APIResourceControllerMixin, APIBaseController):

    def on_get(self, req, resp, **kwargs):
        resp.context['response'] = self.get_response(req, resp, **kwargs)

    def on_post(self, req, resp):
        # schema = self.schema().dump(req.context['request'])
        # req.context['session'].add(self.model(**schema.data))
        # req.context['session'].commit()
        obj = self.schema().load(req.context['request'], session=req.context['session']).data
        req.context['session'].add(obj)
        req.context['session'].commit()

    def on_get_one(self, req, resp, **kwargs):
        resp.context['response'] = self.get_response_one(**kwargs)

    def on_put_one(self, req, resp, **kwargs):
        print ('on_put_one')

    def on_delete_one(self, req, resp, **kwargs):
        print ('on_delete_one')
