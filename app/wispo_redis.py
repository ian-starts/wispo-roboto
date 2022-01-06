import json
from urllib.parse import urlparse

import redis

url = urlparse("redis://:p474a84c390827126039221d0a48c070610bcaefddc6ca3b3bdb4d6b1ab3a0eb0@ec2-63-34-45-212.eu-west-1"
               ".compute.amazonaws.com:32140")
r = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True,
                ssl_cert_reqs=None)


def set_location(user_id, lat, long):
    r.set(user_id, json.dumps({'lat': lat, 'lon': long}), ex=3600*24)


def get_location(user_id):
    location = r.get(user_id).decode()
    return json.loads(location)
