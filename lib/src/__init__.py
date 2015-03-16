
# import logging
# import os
# log_dir = os.getcwd()
# log_dir = log_dir[: log_dir.find('magnet')+len('magnet')]
# log_dir += '/logs/magnet.log'
# # print log_dir
# logging.basicConfig(level=logging.DEBUG, 
# 		   			format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 	datefmt='%a, %d %b %Y %H:%M:%S',
#                 	filename=log_dir,
#                 	filemode='a')

# if __name__ == '__main__':
# 	# print os.getcwd()
# 	pass

# import db
# import people
# __all__ = ['people']
import ConfigParser

cf = ConfigParser.ConfigParser()

#run
cf.read('../etc/magnet.conf')

#test
cf.read('../../etc/magnet.conf')

mongo_host = cf.get('mongo', 'host')
mongo_port = cf.get('mongo', 'port')

debuglog = cf.get('debug','debuglog')

# import sys
# sys.path.insert(0, '.')


if __name__ == '__main__':
	print mongo_host
	print mongo_port