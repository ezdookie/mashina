from mashina.utils.marshmallow import OptCachedNested


def get_nested_fields(Schema, parent=None):
    nested = []
    for f_n, f_o in Schema._declared_fields.items():
        if type(f_o) == OptCachedNested:
            field = f_n if not parent else '%s.%s' % (parent, f_n)
            nested.append(field)
            nested.extend(get_nested_fields(f_o.schema, parent=field))
    return nested
