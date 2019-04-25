from marshmallow import validate, utils, class_registry
from marshmallow.base import SchemaABC
from marshmallow.utils import missing as missing_
from marshmallow.compat import basestring
from marshmallow.fields import Nested

_RECURSIVE_NESTED = 'self'


class OptCachedNested(Nested):

    def __init__(self, nested, cached=True, *args, **kwargs):
        self.nested = nested
        self.cached = cached
        self.__schema = None
        super(OptCachedNested, self).__init__(nested, *args, **kwargs)

    @property
    def schema(self):
        if not self.__schema or not self.cached:
            # Ensure that only parameter is a tuple
            if isinstance(self.only, basestring):
                only = (self.only,)
            else:
                only = self.only

            # Inherit context from parent.
            context = getattr(self.parent, 'context', {})
            if isinstance(self.nested, SchemaABC):
                self.__schema = self.nested
                self.__schema.context.update(context)
            elif isinstance(self.nested, type) and \
                    issubclass(self.nested, SchemaABC):
                self.__schema = self.nested(many=self.many,
                        only=only, exclude=self.exclude, context=context,
                        load_only=self._nested_normalized_option('load_only'),
                        dump_only=self._nested_normalized_option('dump_only'))
            elif isinstance(self.nested, basestring):
                if self.nested == _RECURSIVE_NESTED:
                    parent_class = self.parent.__class__
                    self.__schema = parent_class(many=self.many, only=only,
                            exclude=self.exclude, context=context,
                            load_only=self._nested_normalized_option('load_only'),
                            dump_only=self._nested_normalized_option('dump_only'))
                else:
                    schema_class = class_registry.get_class(self.nested)
                    self.__schema = schema_class(many=self.many,
                            only=only, exclude=self.exclude, context=context,
                            load_only=self._nested_normalized_option('load_only'),
                            dump_only=self._nested_normalized_option('dump_only'))
            else:
                raise ValueError('Nested fields must be passed a '
                                 'Schema, not {0}.'.format(self.nested.__class__))
            self.__schema.ordered = getattr(self.parent, 'ordered', False)
        return self.__schema
