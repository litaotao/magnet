# -*- coding: utf-8 -*-

"""
    test_data.py
    ~~~~~~~~~~~~

    Genernate test data for magnet.

    :Author: taotao.li
    :last updated: Mar.21st.2015
"""

from numpy.random import randint, rand
from functools import wraps
from web import db
from utils import gen_user_context


'''
### Prepare data for test
'''
# test---name
name_lib_str = ['david','weng','john','babala','charles','kevin','ethen',
				'G.G','max','bee','brain','gates','jobs','abama','albert',
				'adam','alan','alexander','barton','barlow','berton','chad',
				'carl','clare','colin','dean','devin','duke','felix','helen']

# test-education
school = range(100)

# test-degree
degree = ['BS','MS','PHD']

# test-birth: just for test, leave this bug along
year = xrange(1950, 2015)
month = xrange(1, 13)
day = xrange(1, 32)

# test-gender
gender = ['man','woman']

# test-location
location = range(100)

# test-field-and-skill
skill = range(120)
filed = range(20)

# test-hobby
hobby = range(50)

# test-tag
tag = range(80)


'''
# A simple wrapper, print func name when been executed.
'''
def print_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print 'start execute {} ...'.format(func.__name__)
        result = func(*args, **kwargs)
        print 'end execute {} ...'.format(func.__name__)
        return result
    return wrapper


@print_name
def init_people():
	'''
	Initialized people database.
	'''
	test_users = []
	test_pwd = ['123456']

	for i in test_users:
		data['age'] = randint(12, 70)
		data['school'] = school[randint(0, len(school))]
		data['degree'] = degree[randint(0, len(degree))]
		data['gender'] = gender[randint(0, len(gender))]
		data['location'] = location[randint(0, len(location))]
		data['location'] = location[randint(0, len(location))]

		data['filed'] = [field[i] for i in randint(0, len(field), 2)]
		data['skill'] = [skill[i] for i in randint(0, len(skill), 5)]
		data['tag'] = [tag[i] for i in randint(0, len(tag), 5)]
		db['user'].insert(gen_user_context(i, test_pwd, data = data))


@print_name
def init_link():
	'''
	Initialized link database.
	'''
	pass


@print_name
def init_link():
	'''
	Initialized link database.
	'''
	pass


@print_name
def init_link():
	'''
	Initialized link database.
	'''
	pass
	# # nodes and links database test data, for echart's convenience
	# node = []
	# links = []
	# for i in range(num_of_people):
	# 	temp = {}
	# 	temp['category'] = randint(1,5)
	# 	temp['name'] = name[i]
	# 	temp['value'] = randint(0,10)
	# 	node.append(temp)
	# # print node
	# # init node database
	# db = client.magnet.node
	# db.remove()
	# for each_node in node:
	# 	db.insert({'category': int(each_node['category']),
	# 			   'name': each_node['name'],
	# 			   'value': int(each_node['value'])})

	# for i in range(num_of_people):
	# 	for j in randint(0, num_of_people, randint(0, num_of_friend)):
	# 		if i != j:
	# 			temp = {}
	# 			temp['source'], temp['target'] = name[i], name[j]
	# 			temp['weight'] = randint(0,10)
	# 			links.append(temp)
	# # print links
	# # init links database
	# db = client.magnet.links
	# db.remove()
	# for each_link in links:
	# 	db.insert({'source': each_link['source'],
	# 			   'target': each_link['target'],
	# 			   'weight': int(each_link['weight'])})

	# client.close()





	