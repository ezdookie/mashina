import json
from mashina.utils.misc import import_string
from mashina.db import Session

session = Session()


def do_seed(file_name):
    data = json.load(open('seeds/%s.json' % file_name, 'r'))

    for dict_obj in data:
        for model_name in dict_obj:
            model = import_string(model_name)
            session.add(model(**dict_obj[model_name]))
            session.commit()

    Session.remove()
