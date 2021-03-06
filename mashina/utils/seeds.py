import yaml

from mashina.db import Session
from mashina.utils.misc import import_string


def do_seed(file_path):
    session = Session()
    document = yaml.full_load(open(file_path, 'r'))
    for app, data in document.items():
        model = import_string(app)
        for row in data:
            session.add(model(**row))
            session.flush()
    session.commit()
    Session.remove()
