from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
from mashina.db import Session
from mashina.utils.misc import import_string


class _Base(object):

    @classmethod
    def all(cls, limit=20, offset=0, order_by=None, filters=None, static_filters=None):
        queryset = Session.query(cls)
        if filters:
            _filters = [getattr(cls, k).like('%%%s%%' % v) for k, v in filters.items()]
            queryset = queryset.filter(or_(*_filters))
        if static_filters:
            _static_filters = {}
            for sf_k, sf_v in static_filters.items():
                if hasattr(cls, sf_k):
                    _static_filters.update({sf_k: sf_v})
                elif 'm2m__' in sf_k:
                    m2m = sf_k.split('__')
                    queryset = queryset.filter(getattr(cls, m2m[1]).any(**{m2m[2]: sf_v}))
            queryset = queryset.filter_by(**_static_filters)
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
