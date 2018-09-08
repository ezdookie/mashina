from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer, or_
from mashina.db import Session


class _Base(object):

    def to_dict(self, include=None, backref=None):
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()}

        if include is not None:
            for attr, relation in self.__mapper__.relationships.items():
                if attr in include:
                    if backref == relation.table:
                        continue
                    value = getattr(self, attr)
                    if value is None:
                        res[relation.key] = None
                    elif isinstance(value.__class__, DeclarativeMeta):
                        res[relation.key] = value.to_dict(backref=self.__table__)
                    else:
                        res[relation.key] = [i.to_dict(backref=self.__table__)
                                             for i in value]

        return res

    # def to_json(self, rel=None):
    #     def extended_encoder(x):
    #         if isinstance(x, datetime):
    #             return x.isoformat()
    #         if isinstance(x, UUID):
    #             return str(x)
    #
    #     if rel is None:
    #         rel = self.RELATIONSHIPS_TO_DICT
    #     return json.dumps(self.to_dict(rel), default=extended_encoder)

    @classmethod
    def all(cls, limit=20, offset=0, order_by=None, filters=None):
        queryset = Session.query(cls)
        if filters:
            _filters = [getattr(cls, k).like('%%%s%%' % v) for k, v in filters.items()]
            queryset = queryset.filter(or_(*_filters))
        if order_by:
            _order_by = getattr(cls, order_by[1:] if order_by.startswith('-') else order_by)
            if order_by.startswith('-'):
                _order_by = _order_by.desc()
            queryset = queryset.order_by(_order_by)
        return queryset.limit(limit).offset(offset).all()

    @classmethod
    def count(cls):
        return Session.query(cls).count()

    @classmethod
    def get_one(cls, id):
        return Session.query(cls).get(id)

    # @classmethod
    # def get_by(cls, **kw):
    #     return Session.query(cls).filter_by(**kw).first()
    #
    # @classmethod
    # def get_or_create(cls, **kw):
    #     r = cls.get_by(**kw)
    #     if r:
    #         return r
    #
    #     return cls.create(**kw)
    #
    # @classmethod
    # def create(cls, **kw):
    #     r = cls(**kw)
    #     Session.add(r)
    #     return r
    #
    # @classmethod
    # def insert(cls, **kw):
    #     Session.execute(cls.__table__.insert(values=kw)).close()
    #
    # @classmethod
    # def insert_many(cls, iter):
    #     Session.execute(cls.__table__.insert(), list(iter)).close()
    #
    # @classmethod
    # def all(cls):
    #     return Session.query(cls).all()
    #
    # @classmethod
    # def count(cls):
    #     return Session.query(cls).count()
    #
    # def delete(self):
    #     Session.delete(self)
    #
    # def refresh(self):
    #     Session.refresh(self)
    #
    # def __repr__(self):
    #     values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in self.__table__.c.keys())
    #     return "%s(%s)" % (self.__class__.__name__, values)
    #


Base = declarative_base(cls=_Base)
