# -*- coding: utf-8 -*-

from sklearn.neighbors import NearestNeighbors as nn
from support import mongo_collect
from distance import *

DEBUG = False
# DEBUG = True

@mongo_collect
def filter_node_criteria(client, name, criteria={}, order=[], k=20):
	'''
	This func is a high-level interface of func filter node.
	parameters:
	client: database link, implemented by a decorator
	name_id: the one who want to do the finding, filtering or discovering
	criteria: the filter criteria, is a python dict object
	order: the filter order, is the sequence of keys in criteria
	filter strategy:
		location: 0-1
		gender: 0-1
		degree: distances matrix
		age: linear algebra
		school: just leave
		skill: Jaccard Similarity
		hobby: Jaccard Similarity
		field: Jaccard Similarity
	'''
	if DEBUG:
		import pdb
		pdb.set_trace()
	### preparation for filtering
	# 1. remove the invalid filter option
	# 2. unify criteria and order
	option = ['location', 'gender', 'degree', 'age', 
			  'school', 'skill', 'hobby', 'field']
	for i in option:
		if i in criteria and i in order and criteria[i] in ['unlimited', '']:
			criteria.pop(i)
			order.remove(i)
		elif i not in order and i in criteria:
			criteria.pop(i)
		else:
			pass
	### start filter
	# a flag marked that it is the first time to do filtering
	name_vec = [-1]		

	# step 1. this step just get the name_id which are corresponded to the 
	# filter criteria just remove the people whose location and gender are 
	# not the same with target's
	for i in order:
		name_vec = filter_node(client, i, criteria[i], name_vec)
		# there is no match items, just return [], [], [] in advance
		if not name_vec:
			return [], [], []

	# step 2. calculate distances in each facet: age, degree, 
	# field, skill, hobby, school
	# age: linear algebra
	# degree: distances matrix
	# age: linear algebra
	# school: just leave
	# skill: Jaccard Similarity
	# hobby: Jaccard Similarity
	# field: Jaccard Similarity
	distances = {}
	res_name = []
	res_distance = []
	for way in order:
		if way not in ['location', 'gender']:
			distances = cal_distances(client, name, name_vec, way)
			if order.index(way) < len(order)-1:
				distances = sorted(distances.items(), key=lambda d:d[1])
				num = min(len(distances)/2, 100)
				name_vec = [distances[i][0] for i in range(num)]
	try:
		distances = sorted(distances.items(), key=lambda d:d[1])
	except:
		# return distances
		pass
	num = min(len(distances), 10)
	for i in range(num):
		res_name.append(distances[i][0])
		res_distance.append(distances[i][1])

	return dict(name=res_name, distance=res_distance)

def filter_node(client, keys, values, scope):
	'''
	This func is the low-level filter function, which is a component of func 
	filter_node_criteria.
	parameters:
	client: database client, implemented by a decorator
	keys: the item which the filter is focusing on
	values: the item's values which the filter is going to filter
	scope: is the range of which we filter from, is the key of this step descent
		   filter algorithm. if scope is [-1], means that we should filter the 
		   whole database, which also prove that it is the first step or first
		   level of the filter is now.
	e.g:
		filter_node_2(client, 'degree', 'PHD', [-1], 2)
		filter_node_2(client, 'degree', 'PHD', [21,22,23,24,25], 2)
		filter_node_2(client, 'location', 'shanghai', [-1], 2)
		filter_node_2(client, 'location', ['shanghai','hangzhou'], [21,22,23,25], 2)
		filter_node_2(client, 'skill', ['skill-01, skill-07'], [-1], 2)
	'''
	db = client.magnet.people

	# judge whether we should query the whole database
	others = []
	if scope[0] != -1:
		for user in db.find({'name': {'$in': scope}}):
			if user[keys] in values or has_common(user[keys], values):
				others.append(user['name'])
	else:
		for user in db.find():
			if user[keys] in values or has_common(user[keys], values):
				others.append(user['name'])

	return others

def has_common(values_1, values_2):
	'''
	return true if values_1 and values_2 have common element, other wise False.
	values_1 and values_2 are both list.
	'''
	if type(values_1) == list:
		for i in values_1:
			if str(i) in values_2:
				return True
	else:
		if values_1 in values_2:
			return True
	return False

def cal_distances(client, name, name_vec, way):
	'''
	'''
	if way == 'age':
		return age_distance(client, name, name_vec)
	elif way == 'degree':
		return degree_distance(client, name, name_vec)
	else:
		return jaccard_similarity(client, name, name_vec, way)


if __name__ == '__main__':
	name = 'kun.xue'
	criteria = {}
	criteria['location'] = 'shanghai'
	criteria['gender'] = 'unlimited'
	criteria['age'] = [24,23,22,21,20,19,18]
	criteria['skill'] = ["infrastructure-skill-1", 
						 "infrastructure-skill-2", 
						 "infrastructure-skill-3", 
						 "infrastructure-skill-4", 
						 "infrastructure-skill-5", 
						 "infrastructure-skill-6" ,
						 "finance-skill-2",
						 "manufacture-skill-1",
						 "manufacture-skill-2",
						 "manufacture-skill-3",
						 "manufacture-skill-6"]
	criteria['hobby'] = ["hobby-16",
						 "hobby-17",
						 "hobby-18",
						 "hobby-19",
						 "hobby-20",
						 "hobby-21",
						 "hobby-22"
						]
	criteria['degree'] = ['BS', 'MS']
	criteria['field'] = 'infrastructure'
	order = ['age']

	res = filter_node_criteria(name, criteria, order, k=10)
	print res