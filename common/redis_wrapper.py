from redislite import Redis
import os
import redis
from erpsms.settings import REDIS_REMOTE_SUPPORT
redisremote = REDIS_REMOTE_SUPPORT


class RedisWrapper():
    def __init__(self):
        pass

    def getredisconnection(self):
        if redisremote:
            self.redis_connection = redis.Redis(
                host='redis-17602.us-east-1-4.3.ec2.garantiadata.com',
                port='17602',
                password='haihai1818')
            return self.redis_connection
        else:
        	workingdir = os.getcwd()
        	self.redis_connection = Redis('%s/data/redis.db' % (workingdir))
        	return self.redis_connection
