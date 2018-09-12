from importlib import import_module


def import_string(dotted_path, silent=False):
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
        module = import_module(module_path)
        attr = getattr(module, class_name)
    except ModuleNotFoundError:
        if not silent:
            raise ModuleNotFoundError
        attr = None
    except AttributeError:
        if not silent:
            raise AttributeError
        attr = None
    return attr
