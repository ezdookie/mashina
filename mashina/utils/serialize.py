from mashina.utils.marshmallow import CustomNested


def get_nested_fields(Schema, parent=None):
    nested = []
    for f_n, f_o in Schema._declared_fields.items():
        if hasattr(f_o, 'nested'):
            field = f_n if not parent else '%s.%s' % (parent, f_n)
            nested.append(field)
            nested.extend(get_nested_fields(f_o.schema, parent=field))
    return nested
