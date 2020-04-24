class APIListMixin(object):
    def list(self, req, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(), req, **kwargs)
        page = self.paginate_queryset(queryset, req)
        serializer = self.get_serializer(many=True)
        return self.get_paginated_response(serializer.dump(page))


class APICreateMixin(object):
    def create(self, req, **kwargs):
        serializer = self.get_serializer()
        payload = self.get_payload(req, **kwargs)
        load_data = serializer.load(payload)
        serializer.save(load_data)
        return serializer.dump(load_data)


class APIRetrieveMixin(object):
    def retrieve(self, req, **kwargs):
        instance = self.get_object(req, **kwargs)
        serializer = self.get_serializer()
        return serializer.dump(instance)


class APIUpdateMixin(object):
    def partial_update(self, req, **kwargs):
        instance = self.get_object(req, **kwargs)
        serializer = self.get_serializer(instance=instance, partial=True)
        load_data = serializer.load(req.context['request'])
        serializer.save(load_data)
        return serializer.dump(load_data)


class APIDestroyMixin(object):
    def destroy(self, req, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(), req, **kwargs)
        queryset.delete()
        req.context['session'].commit()
        return True
