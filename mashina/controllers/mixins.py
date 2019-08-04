import falcon
from mashina.utils.serialize import get_nested_fields


class APIListMixin(object):

    def get_response(self, **kwargs):
        self.collect_get_params(**kwargs)
        self.objects_count, results = self.get_results()
        return {
            'count': self.objects_count,
            'next': self.get_next_page(),
            'previous': self.get_prev_page(),
            'results': results
        }

    def get_results(self):
        schema = self.get_schema(
            many=True,
            exclude=[e for e in get_nested_fields(self.Schema) \
                if e not in self.query_params['include']]
        )
        objects_count, objs = self.Schema.Meta.model.all(
            order_by=self.query_params['sort'],
            limit=self.query_params['limit'],
            offset=self.query_params['offset'],
            filters=self.query_params.get('filters'),
            static_filters=self.query_params['static_filters']
        )
        return objects_count, schema.dump(objs).data

    def collect_get_params(self, **kwargs):
        if hasattr(self.Schema.Meta, 'filter_fields'):
            self.query_params['filters'] = {k: v for k, v in self.req.params.items() \
                if k in self.Schema.Meta.filter_fields}
        self.query_params['sort'] = self.req.get_param('sort', default='id')
        self.query_params['include'] = self.req.get_param_as_list('include', default=[])
        self.query_params['limit'] = self.req.get_param_as_int('limit', default=20)
        self.query_params['offset'] = self.req.get_param_as_int('offset', default=0)
        self.query_params['static_filters'] = {**kwargs, **self.req.context.get('static_filters', {})}

    def get_next_page(self):
        limit, offset = self.query_params['limit'], self.query_params['offset']+self.query_params['limit']
        return self.get_nextprev({
            'limit': limit, 'offset': offset
        }) if offset < self.objects_count else None

    def get_prev_page(self):
        limit, offset = self.query_params['limit'], max(0, self.query_params['offset']-self.query_params['limit'])
        return self.get_nextprev({
            'limit': limit, 'offset': offset
        }) if self.query_params['offset'] > 0 else None

    def get_nextprev(self, params):
        absolute_url = '{scheme}://{netloc}'.format(
            scheme=self.req.scheme,
            netloc=self.req.netloc
        )
        querystring = '?'
        for k, v in params.items():
            querystring += '%s=%s&' % (k, v)
        return '{absolute_url}{path}{querystring}'.format(
            absolute_url=absolute_url,
            path=self.req.path,
            querystring=querystring[:-1]
        )


class APICreateMixin(object):

    def get_post_response(self, **kwargs):
        ctx = self.req.context
        self.created_obj, schema = self.validate(ctx['request'])
        ctx['session'].add(self.created_obj)
        ctx['session'].commit()
        return schema.dump(self.created_obj).data


class APIRetrieveMixin(object):

    def get_one_response(self, **kwargs):
        self.collect_get_one_params()
        return self.get_one_result(**kwargs)

    def get_one_queryset(self, **kwargs):
        queryset = None
        model = self.Schema.Meta.model
        table_name = model.__table__.name.lower()
        for param_name, param_value in kwargs.items():
            if '_' in param_name:
                _table, _filter_field = param_name.split('_', 1)
                if table_name == _table:
                    queryset = model.filter(getattr(model, _filter_field) == param_value)
        return queryset

    def get_one_result(self, **kwargs):
        obj = self.get_one_queryset(**kwargs).one_or_none()
        if obj is not None:
            schema = self.Schema(exclude=[e for e in get_nested_fields(self.Schema) \
                if e not in self.query_params['include']])
            return schema.dump(obj).data
        else:
            raise falcon.HTTPNotFound

    def collect_get_one_params(self, **kwargs):
        self.query_params['include'] = self.req.get_param_as_list('include', default=[])


class APIUpdateMixin(object):

    def get_put_response(self, **kwargs):
        _updated_obj = self.get_one_queryset(**kwargs).one_or_none()
        ctx = self.req.context
        if _updated_obj is not None:
            self.updated_obj, schema = self.validate(ctx['request'], instance=_updated_obj, partial=True)
            ctx['session'].add(self.updated_obj)
            ctx['session'].commit()
            return schema.dump(self.updated_obj).data
        else:
            raise falcon.HTTPNotFound


class APIDeleteMixin(object):

    def get_delete_response(self, **kwargs):
        session = self.req.context['session']
        self.deleted_obj = self.get_one_queryset(**kwargs).one_or_none()
        session.delete(self.deleted_obj)
        session.commit()
