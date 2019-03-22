import falcon


class APICollectionGETMixin(object):
    query_params = {}
    objects_count = 0

    def objects_to_list(self, objects):
        # schema = self.Schema()
        # return [schema.dump(obj).data for obj in objects]
        return [obj.to_dict(include=self.query_params.get('include')) for obj in objects]

    def get_querystring(self, params):
        querystring = '?'
        for k, v in params.items():
            querystring += '%s=%s&' % (k, v)
        return querystring[:-1]

    def get_absolute_url(self, req):
        return '{scheme}://{netloc}'.format(
            scheme=req.scheme,
            netloc=req.netloc
        )

    def get_next_page(self, req):
        limit, offset = self.query_params['limit'], self.query_params['offset']+self.query_params['limit']
        return self.get_nextprev(req, {
            'limit': limit, 'offset': offset
        }) if offset < self.objects_count else None

    def get_prev_page(self, req):
        limit, offset = self.query_params['limit'], max(0, self.query_params['offset']-self.query_params['limit'])
        return self.get_nextprev(req, {
            'limit': limit, 'offset': offset
        }) if self.query_params['offset'] > 0 else None

    def get_nextprev(self, req, params):
        return '{absolute_url}{path}{querystring}'.format(
            absolute_url=self.get_absolute_url(req),
            path=req.path,
            querystring=self.get_querystring(params)
        )

    def get_results(self):
        count, query_results = self.model.all(
            order_by=self.query_params['sort'],
            limit=self.query_params['limit'],
            offset=self.query_params['offset'],
            filters=self.query_params.get('filters'),
            exact_filters=self.query_params['exact_filters']
        )
        return count, self.objects_to_list(query_results)

    def collect_params(self, req):
        self.query_params['sort'] = req.get_param('sort', default='id')
        req.get_param_as_list('include', store=self.query_params)
        req.get_param_as_int('limit', store=self.query_params)
        req.get_param_as_int('offset', store=self.query_params)

    def add_exact_filters(self, **kwargs):
        self.query_params['exact_filters'] = kwargs

    def get_response(self, req, resp, **kwargs):
        self.collect_params(req)
        if hasattr(self.Schema.Meta, 'filter_fields'):
            self.query_params['filters'] = {k: v for k, v in req.params.items() if k in self.Schema.Meta.filter_fields}
        self.add_exact_filters(**kwargs)
        self.add_exact_filters(**req.context['exact_filters'])
        count, results = self.get_results()
        return {
            'count': count,
            'next': self.get_next_page(req),
            'previous': self.get_prev_page(req),
            'results': results
        }

    def on_get(self, req, resp, **kwargs):
        resp.context['response'] = self.get_response(req, resp, **kwargs)


class APICollectionPOSTMixin(object):
    def add_obj(self, data, schema, ignore=False):
        obj = self.validate(data, schema, ignore)
        session = self.req.context['session']
        session.add(obj)
        return obj

    def add_child(self, field, data, schema, ignore=False):
        obj = self.validate(data, schema, ignore)
        getattr(self.obj, field).append(obj)
        return obj

    def commit(self):
        session = self.req.context['session']
        session.commit()

    def validate(self, data, schema, ignore):
        marsh = schema.load(data, partial=ignore, session=self.req.context['session'])
        if marsh.errors:
            raise falcon.HTTPBadRequest('Validation error', marsh.errors)
        return marsh.data

    def get_post_response(self, **kwargs):
        ctx = self.req.context
        ctx['request'].update(kwargs)
        self.obj = self.add_obj(ctx['request'], self.Schema())
        self.commit()
        return self.obj.to_dict()


class APIResourceControllerMixin(object):
    def get_id_keyword(self):
        return '%s_id' % self.model.__table__.name.lower()

    def get_result_one(self, id):
        return self.model.get_one(id).to_dict()

    def get_one_response(self, **kwargs):
        return self.get_result_one(kwargs.get(self.get_id_keyword()))
