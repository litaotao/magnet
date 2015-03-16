# -*- coding: utf-8 -*-

from test_data import field_skill, school, \
					  degree, gender, location, hobby

from contact import name_lib_str

num_of_people = len(name_lib_str)
num_of_friend = 8

### Initial test database
def init_node_links():
	'''
	Initialized database using all test data
	'''
	from numpy.random import randint, rand
	from pymongo import MongoClient
	
	client = MongoClient('localhost', 27017)
	name = []
	name_id = []
	tag = []
	know_to = {}
	know_from = {}

	for i in range(num_of_people):
		name.append(name_lib_str[i])
		name_id.append(i)

	# init people database
	db = client.magnet.people
	db.remove()
	for i in range(num_of_people):
	    field_index = randint(0, len(field_skill.keys()))
	    field  = field_skill.keys()[field_index]
	    num_skill = len(field_skill[field])
	    skill = [field_skill[field][j] for j in randint(0,num_skill,randint(0,num_skill))]

	    db.insert( {'name': name[i],   # 'name': name_id[i]
	    			'name_id': name_id[i],
	    			'origin_pr': 1,
	    			'new_pr': 1,
	    			'age': randint(12, 70),
	    			'school': school[randint(0, len(school))],
	    			'degree': degree[randint(0, len(degree))],
	    			'gender': gender[randint(0, len(gender))],
	    			'location': 'shanghai',
	    			'field': field,
	    			'hobby': hobby[randint(0, len(hobby))],
	    			'skill': skill,
	    			'tag': tag,
	    			'ratetimes': 0,
	    			'people_rate_me': [],
	    			'pwd': ['12345678']
	    			} )

	# nodes and links database test data, for echart's convenience
	node = []
	links = []
	for i in range(num_of_people):
		temp = {}
		temp['category'] = randint(1,5)
		temp['name'] = name[i]
		temp['value'] = randint(0,10)
		node.append(temp)
	# print node
	# init node database
	db = client.magnet.node
	db.remove()
	for each_node in node:
		db.insert({'category': int(each_node['category']),
				   'name': each_node['name'],
				   'value': int(each_node['value'])})

	for i in range(num_of_people):
		for j in randint(0, num_of_people, randint(0, num_of_friend)):
			if i != j:
				temp = {}
				temp['source'], temp['target'] = name[i], name[j]
				temp['weight'] = randint(0,10)
				links.append(temp)
	# print links
	# init links database
	db = client.magnet.links
	db.remove()
	for each_link in links:
		db.insert({'source': each_link['source'],
				   'target': each_link['target'],
				   'weight': int(each_link['weight'])})

	client.close()

def vote_db():
	'''
	'''
	from numpy.random import randint, rand
	from pymongo import MongoClient
	
	client = MongoClient('localhost', 27017)
	db = client.magnet.vote
	db.remove()

	client.close()

if __name__ == '__main__':
	init_node_links()
	vote_db()

