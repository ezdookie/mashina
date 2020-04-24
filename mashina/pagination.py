class LimitOffsetPagination(object):
    limit = 10
    offset = 0

    def __init__(self, req):
        self.req = req
        self.count = None

    def paginate_queryset(self, queryset):
        self.count = queryset.count()
        self.limit = self.req.get_param_as_int('limit', default=self.limit)
        self.offset = self.req.get_param_as_int('offset', default=self.offset)
        return queryset.limit(self.limit).offset(self.offset)

    def get_paginated_response(self, data):
        return {
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_prev_link(),
            'results': data
        }

    def get_link(self, limit, offset):
        absolute_url = '{scheme}://{netloc}'.format(
            scheme=self.req.scheme,
            netloc=self.req.netloc
        )
        querystring = '?limit=%s&offset=%s' % (limit, offset)
        return '%s%s%s' % (absolute_url, self.req.path, querystring)

    def get_next_link(self):
        return self.get_link(
            limit=self.limit,
            offset=self.offset + self.limit
        ) if self.count > self.offset + self.limit else None

    def get_prev_link(self):
        return self.get_link(
            limit=self.limit,
            offset=max(0, self.offset - self.limit)
        ) if self.offset > 0 else None
