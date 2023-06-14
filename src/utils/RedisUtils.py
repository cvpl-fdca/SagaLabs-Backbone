import redis
import os


class RedisUtils:
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    print(redis_host)

    def __init__(self, host=redis_host, port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db)

    def get_client(self):
        return self.client

    def set_value(self, key, value):
        self.client.set(key, value)

    def get_value(self, key):
        return self.client.get(key)
