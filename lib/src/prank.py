
# from pymongo import MongoClient
from support import *
# from __init__ import logging

# @log_func(logging)
@mongo_collect
def get_score(client, name_id, from_id):
	'''
	get score from some one call name_id
	'''
	# get score name_id gained from from_id
	db = client.magnet.links
	score = None
	for one in db.find( {'source': from_id, 'target': name_id}):
		score = one['weight']

	if not score:
		return -1
	# get the number of one
	db = client.magnet.links
	link = 0
	for one in db.find({'source': from_id}):
		link += 1

	if link!=0:
		return float(score)/link
	else:
		return float(score)
	return -1

# @log_func(logging)
@mongo_collect
def get_origin_pr(client, name_id):
	'''
	get one's origin pr value
	'''
	db = client.magnet.people
	for one in db.find( {'name_id':name_id}):
		return one['origin_pr']

# @log_func
@mongo_collect
def calc_origin_rank(client, name_id):
	'''
	calculate one's origin rank, using page rank algorithm
	'''
	db_link = client.magnet.links
	db_people = client.magnet.people

	score = 0.0 
	for each in db_link.find({'target': name_id}): #each one know name_id
		score += get_score(name_id, each['source'])
	origin_pr = 0.15 + 0.85*score

	db_people.update( {'name_id':name_id},
				{'$set':
					{'origin_pr':origin_pr}
				})
	# client.close()
	return origin_pr

# @log_func
@mongo_collect
def calibrate_origin_rank(client):
	'''
	calibrate_origin_rank, that's recalculate all the people's origin_pr
	'''
	db = client.magnet.people
	for i in db.find():
		calc_origin_rank(i['name_id'])

# @log_func
@mongo_collect
def calc_new_score(client, name_id, from_id):
	'''
	calculate new score for someone, is a improved method to give someone
	a score, which combining the traditional page rank and regulation 
	algorithm.
	'''
	# find the value vector giving by from_id
	db = client.magnet.links
	search_range = []
	score = 0.0
	for one in db.find({'source': from_id}):
		search_range.append(one['weight'])
		if one['target'] == name_id:
			score = one['weight']

	# find the from_id's score calculated	
	db = client.magnet.people
	pr = 0.0
	for one in db.find({'name': from_id}):
		pr = one['new_pr']

	temp = percent_rank(search_range, score)
	return temp+0.1*pr

def percent_rank(search_range, score):
	'''
	calculate the percent rank of one score in a score vector.
	'''
	if score not in search_range:
		search_range.append(score)
	search_range.sort()
	if score < search_range[0]:
		return 0
	elif score > search_range[len(search_range)-1]:
		return 1.0
	else:
		smaller = 0
		for i in search_range:
			if i <= score:
				smaller += 1
		return float(smaller)/len(search_range)

# @log_func
@mongo_collect
def calc_new_pr(client, name_id):
	'''
	calculate one's new score using a method which combining
	page rank algorithm and regulation algorithm.
	'''
	db_link = client.magnet.links
	db_people = client.magnet.people

	score = 0.0 
	for each in db_link.find({'target': name_id}): #each one know name_id
		score += calc_new_score(name_id, each['source'])
		# print each['source'], score

	new_pr = 0.15 + 0.85*score

	db_people.update( {'name': name_id},
						{'$set':
							{'new_pr': new_pr}
					})
	return new_pr

# @log_func
@mongo_collect
def calibrate_new_pr(client):
	'''
	calibrate_new_pr, that's recalculate all the people's new_pr
	'''
	db = client.magnet.people
	for i in db.find():
		print calc_new_pr(i['name'])

@mongo_collect
def simulate_self_balance(client):
	'''
	simulate the real operation in the real world.
	just simulating one's setting score behavior.
	'''
	from numpy.random import randint
	db_people = client.magnet.people
	db_links = client.magnet.links
	# for each one in the database
	for i in db_people.find():
		tmp_user = i['name']
		# for every people tmp_user knows in his relation
		for j in db_links.find({'source': tmp_user}):
			score = randint(0,100)/10.
			db_links.update({'source': tmp_user, 'target': j['target']},
					  {'$set':
					  		{'weight': score}
					  })


if __name__  == '__main__':
	# print get_score(2, 7)
	# print calc_origin_rank(2)
	# calibrate_origin_rank()
	simulate_self_balance()
	calibrate_new_pr()
	# print calc_new_pr('yaodong.gong')
	pass



