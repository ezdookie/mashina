from mashina.models import BaseModel


def get_class_by_tablename(tablename):
    for c in BaseModel._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c
