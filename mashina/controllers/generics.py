import falcon
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from mashina.controllers.mixins import APIListMixin, APICreateMixin, APIRetrieveMixin, APIUpdateMixin, APIDestroyMixin
from mashina.filters import SqlAlchemyFilter
from mashina.pagination import LimitOffsetPagination
from mashina.utils.db import get_class_by_tablename


class APIBaseController(object):
    Serializer = None
    paginator = None

    def __init__(self, Serializer=None):
        if Serializer is not None:
            self.Serializer = Serializer

    def get_payload(self, req, **kwargs):
        data = req.context['request']
        for param_name, param_value in kwargs.items():
            if '__' in param_name:
                table_name, field = param_name.split('__')
                if field != 'id':
                    model_class = get_class_by_tablename(table_name)
                    try:
                        model_instance = model_class.objects().filter_by(**{field: param_value}).one()
                    except (NoResultFound, MultipleResultsFound):
                        raise falcon.HTTPNotFound()
                    param_value = str(model_instance.id)
                data['%s_id' % table_name] = param_value
        return data

    def get_object(self, req, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(), req, **kwargs)
        try:
            return queryset.one()
        except (NoResultFound, MultipleResultsFound):
            raise falcon.HTTPNotFound()

    def get_serializer(self, *args, **kwargs):
        serializer = self.Serializer(*args, **kwargs)
        return serializer

    def get_queryset(self):
        return self.Serializer.Meta.model.objects()

    def filter_queryset(self, queryset, req, **kwargs):
        sqlalchemy_filter = SqlAlchemyFilter(req, self.Serializer)
        return sqlalchemy_filter.filter_queryset(queryset, **kwargs)

    def paginate_queryset(self, queryset, req):
        self.paginator = LimitOffsetPagination(req)
        return self.paginator.paginate_queryset(queryset)

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)


class APICreateController(APICreateMixin, APIBaseController):
    def on_post(self, req, resp, **kwargs):
        resp.context['response'] = self.create(req, **kwargs)


class APIListController(APIListMixin, APIBaseController):
    def on_get(self, req, resp, **kwargs):
        resp.context['response'] = self.list(req, **kwargs)


class APIRetrieveController(APIRetrieveMixin, APIBaseController):
    def on_get(self, req, resp, **kwargs):
        resp.context['response'] = self.retrieve(req, **kwargs)


class APIDestroyController(APIDestroyMixin, APIBaseController):
    def on_delete(self, req, resp, **kwargs):
        resp.context['response'] = self.destroy(req, **kwargs)


class APIUpdateController(APIUpdateMixin, APIBaseController):
    def on_patch(self, req, resp, **kwargs):
        resp.context['response'] = self.partial_update(req, **kwargs)


class APIListCreateController(APIListMixin, APICreateMixin, APIBaseController):
    def on_get(self, req, resp, **kwargs):
        resp.context['response'] = self.list(req, **kwargs)

    def on_post(self, req, resp, **kwargs):
        resp.context['response'] = self.create(req, **kwargs)


class APIRetrieveUpdateController(APIRetrieveMixin, APIUpdateMixin, APIBaseController):
    def on_get(self, req, resp, **kwargs):
        resp.context['response'] = self.retrieve(req, **kwargs)

    def on_patch(self, req, resp, **kwargs):
        resp.context['response'] = self.partial_update(req, **kwargs)


class APIRetrieveDestroyController(APIRetrieveMixin, APIDestroyMixin, APIBaseController):
    def on_get(self, req, resp, **kwargs):
        resp.context['response'] = self.retrieve(req, **kwargs)

    def on_delete(self, req, resp, **kwargs):
        resp.context['response'] = self.destroy(req, **kwargs)


class APIRetrieveUpdateDestroyController(APIRetrieveMixin, APIUpdateMixin, APIDestroyMixin, APIBaseController):
    def on_get(self, req, resp, **kwargs):
        resp.context['response'] = self.retrieve(req, **kwargs)

    def on_patch(self, req, resp, **kwargs):
        resp.context['response'] = self.partial_update(req, **kwargs)

    def on_delete(self, req, resp, **kwargs):
        resp.context['response'] = self.destroy(req, **kwargs)
