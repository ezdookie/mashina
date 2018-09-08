import falcon


class ${name}Resource(object):

    def on_get(self, req, resp):
        resp.context['response'] = {
            'foo': 'bar'
        }
