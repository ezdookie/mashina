import json
import models
from mashina.db import Session

session = Session()


def do_seeds():
    data = json.load(open('seeds/base.json', 'r'))

    for dict_obj in data:
        for model_name in dict_obj:
            model = getattr(models, model_name)
            session.add(model(**dict_obj[model_name]))
            session.commit()

    Session.remove()
