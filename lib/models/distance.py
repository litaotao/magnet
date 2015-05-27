# -*- coding: utf-8 -*-

def age_distance(client, name, name_vec):
	'''
	'''
	res = {}
	db = client.magnet.people
	my_age = db.find_one({'name': name}, {'age': 1})['age']
	for i in db.find({'name': {'$in': name_vec}}, {'age': 1, 'name': 1}):
		res[i['name']] = abs(my_age-i['age'])/10. 
	return res

def degree_distance(client, name, name_vec):
	'''
	'''
	metric = dict(BS=0, MS=3, PHD=5)
	res = {}
	db = client.magnet.people
	my_degree = db.find_one({'name': name}, {'degree': 1})['degree']
	for i in db.find({'name': {'$in': name_vec}}, {'degree': 1, 'name': 1}):
		res[i['name']] = abs(metric[my_degree]-metric[i['degree']])/10. 
	return res

def jaccard_similarity(client, name, name_vec, way):
	'''
	'''
	res = {}
	db = client.magnet.people
	me = db.find_one({'name': name}, {way: 1})[way]

	for i in db.find({'name': {'$in': name_vec}}, {way: 1, 'name': 1}):
		total = list(me) + list(i[way])
		common = [j for j in total if total.count(j)>1]
		common = set(common)
		total = set(total)
		res[i['name']] = float(len(common))/(len(total)+1)
	return res

