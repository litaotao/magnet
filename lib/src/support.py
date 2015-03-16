# -*- coding: utf-8 -*-

from functools import wraps
from pymongo import MongoClient
from __init__ import mongo_host, mongo_port
# import inspect
# import time
# from __init__ import logging


# decorator for logger using module logging
# def log_func(log, level='debug'):
# 	def wrap(func):
# 		def func_wrapper(*args, **kwargs):
# 			log.debug("Into function %s: " %func)
# 			if level == 'debug':
	# 			for i, arg in enumerate(args):
	# 				log.debug('\ttuple args-%d: %s' %(i+1, arg))
	# 			for k, v in enumerate(kwargs):
	# 				log.debug('\tdict  args-%d: %s->%s' %(k, v, kwargs[v]))
	# 		try:
	# 			res = func(*args, **kwargs)
	# 			log.debug('func %s return %s' %(func, res))
	# 			log.debug('Out function %s: ' %func)
	# 			log.debug("\n---------------------------\n")
	# 			return res
	# 		except:
	# 			log.debug('func %s exception' %func)
	# 			log.exception('exception info')
	# 			return -400
	# 	return func_wrapper
	# return wrap

# decorator for mongo db collection and close
def mongo_collect(fn):
	@wraps(fn)
	def inner(*args, **kwargs):
		client = MongoClient(mongo_host, int(mongo_port))
		res = fn(client, *args, **kwargs)
		client.close()
		return res
	return inner

# if __name__ == '__main__':
# 	from __init__ import mongo_port
# 	print mongo_port