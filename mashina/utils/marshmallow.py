from marshmallow import class_registry
from marshmallow.base import SchemaABC
from marshmallow.compat import basestring
from marshmallow.fields import Nested

_RECURSIVE_NESTED = 'self'


class CustomNested(Nested):
    @property
    def schema(self):
        # Ensure that only parameter is a tuple
        if isinstance(self.only, basestring):
            only = (self.only,)
        else:
            only = self.only

        # Inherit context from parent.
        context = getattr(self.parent, 'context', {})
        if isinstance(self.nested, SchemaABC):
            _schema = self.nested
            _schema.context.update(context)
        elif isinstance(self.nested, type) and \
                issubclass(self.nested, SchemaABC):
            _schema = self.nested(many=self.many,
                    only=only, exclude=self.exclude, context=context,
                    load_only=self._nested_normalized_option('load_only'),
                    dump_only=self._nested_normalized_option('dump_only'))
        elif isinstance(self.nested, basestring):
            if self.nested == _RECURSIVE_NESTED:
                parent_class = self.parent.__class__
                _schema = parent_class(many=self.many, only=only,
                        exclude=self.exclude, context=context,
                        load_only=self._nested_normalized_option('load_only'),
                        dump_only=self._nested_normalized_option('dump_only'))
            else:
                schema_class = class_registry.get_class(self.nested)
                _schema = schema_class(many=self.many,
                        only=only, exclude=self.exclude, context=context,
                        load_only=self._nested_normalized_option('load_only'),
                        dump_only=self._nested_normalized_option('dump_only'))
        else:
            raise ValueError('Nested fields must be passed a '
                             'Schema, not {0}.'.format(self.nested.__class__))
        _schema.ordered = getattr(self.parent, 'ordered', False)
        return _schema

    def get_value(self, *args, **kwargs):
        self.attribute = None
        return super(CustomNested, self).get_value(*args, **kwargs)

    def deserialize(self, *args, **kwargs):
        if not self.many:
            self.attribute = '%s_id' % self.name
        return super(CustomNested, self).deserialize(*args, **kwargs)
