import uuid
import datetime
import decimal
import uuid


def json_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return str(obj)
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    elif isinstance(obj, uuid.UUID):
        return str(obj)

    raise TypeError('Cannot serialize {!r} (type {})'.format(obj, type(obj)))
