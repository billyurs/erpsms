from redislite import Redis
import os
import redis
import logging
logger_stats = logging.getLogger('erpsms_stats')

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
        	logger_stats.info('Redis path :\t %s erpsms/data/redis.db' % (workingdir))
        	self.redis_connection = Redis('%s/erpsms/data/redis.db' % (workingdir))
        	return self.redis_connection
