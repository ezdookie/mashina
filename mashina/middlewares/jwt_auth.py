import jwt
import redis
from config import settings


class JWTAuthMiddleware(object):
    def process_resource(self, req, resp, resource, params):
        # try:
        #     r = redis.StrictRedis(host='redis', db=0)
        #     token = req.auth.split(' ')
        #     token = r.get(token[1])
        # except:
        #     token = None
        token = req.auth
        if token is not None:
            req.context['auth'] = jwt.decode(token, settings.JWT_SECRET_KEY, algorithm='HS256')
