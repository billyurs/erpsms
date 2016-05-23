from redislite import Redis
import os
def getredisconnection():
	"""
	Returns the redis cache connection
	"""
	workingdir = os.getcwd()
	redis_connection = Redis('%s/data/redis.db'%(workingdir))
	if redis_connection:
		return redis_connection