import json
from mashina.utils.misc import import_string
from mashina.db import Session

session = Session()


def do_seeds():
    data = json.load(open('seeds/base.json', 'r'))

    for dict_obj in data:
        for model in dict_obj:
            model = import_string(model)
            session.add(model(**dict_obj[model_name]))
            session.commit()

    Session.remove()
