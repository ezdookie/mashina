import jwt
from config import settings


class JWTAuthMiddleware(object):
    def process_resource(self, req, resp, resource, params):
        token = req.auth
        if token is not None:
            try:
                req.context['auth'] = jwt.decode(token, settings.JWT_SECRET_KEY, algorithm='HS256')
            except:
                pass
