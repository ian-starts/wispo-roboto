import json

import redis


def set_location(user_id, lat, long):
    r = redis.from_url(
        "redis://:p474a84c390827126039221d0a48c070610bcaefddc6ca3b3bdb4d6b1ab3a0eb0@ec2-54-74-153-24.eu-west-1"
        ".compute.amazonaws.com:17940")
    r.set(user_id, json.dumps({'lat': lat, 'lon': long}))


def get_location(user_id):
    r = redis.from_url(
        "redis://:p474a84c390827126039221d0a48c070610bcaefddc6ca3b3bdb4d6b1ab3a0eb0@ec2-54-74-153-24.eu-west-1"
        ".compute.amazonaws.com:17940")
    location = r.get(user_id).decode()
    return json.loads(location)
