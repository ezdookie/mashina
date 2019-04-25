from mashina.controllers.base import APIBaseController
from mashina.controllers.mixins import APIListMixin, APICreateMixin, \
    APIRetrieveMixin, APIUpdateMixin


class APIListCreateController(APICreateMixin, APIListMixin, APIBaseController):

    def on_get(self, req, resp, **kwargs):
        self.resp.context['response'] = self.get_response(**kwargs)

    def on_post(self, req, resp, **kwargs):
        resp.context['response'] = self.get_post_response(**kwargs)


class APIRUDController(APIUpdateMixin, APIRetrieveMixin, APIBaseController):

    def on_get(self, req, resp, **kwargs):
        resp.context['response'] = self.get_one_response(**kwargs)

    def on_put(self, req, resp, **kwargs):
        resp.context['response'] = self.get_put_response(**kwargs)
