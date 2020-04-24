import falcon
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from mashina.utils.db import get_class_by_tablename


class SqlAlchemyFilter(object):

    def __init__(self, req, Serializer):
        self.req = req
        self.Serializer = Serializer

    def filter_queryset(self, queryset, **kwargs):
        filters = []

        # ordering filter
        ordering_values = self.req.params.pop('ordering', None)
        if ordering_values is not None:
            for ordering_value in ordering_values.split(','):
                _order_by = getattr(self.Serializer.Meta.model, ordering_value.replace('-', ''))
                if ordering_value.startswith('-'):
                    _order_by = _order_by.desc()
                queryset = queryset.order_by(_order_by)

        # url params filter
        if hasattr(self.Serializer.Meta, 'filterset_fields'):
            for filter_field in self.Serializer.Meta.filterset_fields:
                if filter_field in self.req.params:
                    filters.append(
                        getattr(self.Serializer.Meta.model, filter_field) == self.req.params.get(filter_field))

        # url kwargs filter
        for param_name, param_value in kwargs.items():
            if '__' in param_name:
                table_name, field = param_name.split('__')
                if table_name == self.Serializer.Meta.model.__tablename__:
                    filters.append(getattr(self.Serializer.Meta.model, field) == param_value)
                else:
                    if field != 'id':
                        model_class = get_class_by_tablename(table_name)
                        try:
                            model_instance = model_class.objects().filter_by(**{field: param_value}).one()
                        except (NoResultFound, MultipleResultsFound):
                            raise falcon.HTTPNotFound()
                        param_value = model_instance.id
                    filters.append(getattr(self.Serializer.Meta.model, '%s_id' % table_name) == param_value)

        return queryset.filter(*filters) if filters else queryset
