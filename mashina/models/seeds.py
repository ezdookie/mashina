import yaml
from mashina.utils.misc import import_string
from mashina.db import Session

session = Session()


def do_seed(file_path):
    document = yaml.full_load(open('%s.yml' % file_path, 'r'))
    for app, data in document.items():
        model = import_string(app)
        for row in data:
            session.add(model(**row))
            session.flush()
    session.commit()
    Session.remove()
