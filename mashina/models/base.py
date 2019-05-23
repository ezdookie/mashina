from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
from mashina.db import Session


class _Base(object):

    @classmethod
    def all(cls, limit=20, offset=0, order_by=None, filters=None, static_filters=None):
        queryset = Session.query(cls)
        if filters:
            _filters = [getattr(cls, k).like('%%%s%%' % v) for k, v in filters.items()]
            queryset = queryset.filter(or_(*_filters))
        if static_filters:
            static_filters = {k: v for k, v in static_filters.items() if hasattr(cls, k)}
            queryset = queryset.filter_by(**static_filters)
        if order_by:
            _order_by = getattr(cls, order_by[1:] if order_by.startswith('-') else order_by)
            if order_by.startswith('-'):
                _order_by = _order_by.desc()
            queryset = queryset.order_by(_order_by)
        return queryset.count(), queryset.limit(limit).offset(offset)

    @classmethod
    def get_one(cls, id):
        return Session.query(cls).get(id)

    @classmethod
    def get_by(cls, **kwargs):
        return Session.query(cls).filter_by(**kwargs).one_or_none()

    @classmethod
    def filter(cls, *args):
        return Session.query(cls).filter(*args)

    @classmethod
    def filter_by(cls, **kwargs):
        return Session.query(cls).filter_by(**kwargs)


Base = declarative_base(cls=_Base)
