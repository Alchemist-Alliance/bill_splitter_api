from constant import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, KEY
from redis import Redis

DEFAULT_TIME = 900

redisClient = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)


def add_to_redis(Entity, data):
    redisClient.json().set(f"{Entity}-{data[KEY]}", '$', data)
    redisClient.expire(name=f"{Entity}-{data[KEY]}", time=DEFAULT_TIME)
    

def fetch_from_redis(Entity, key) -> dict:
    return redisClient.json().get(name=f"{Entity}-{key}")

def remove_from_redis(Entity, key) -> dict:
    return redisClient.json().delete(name=f"{Entity}-{key}")