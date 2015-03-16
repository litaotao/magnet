# -*- coding: utf-8 -*-
from support import mongo_collect

@mongo_collect
def  calculate_rank(client, name, rank_way):
	'''
	return the rank result by rank_way
	rank_way_number - rank_way
	0 - place - location
	1 - age
	2 - gender
	3 - degree
	4 - skill
	5 - field
	6 - school
	'''
	db = client.magnet.people
	rank_dict = ['location', 'age', 'gender', 
				 'degree', 'skill', 'field', 'school']
	way = rank_dict[rank_way]
	usr_criteria = ''
	for i in db.find({'name': name}):
		usr_criteria = i

	res = db.find({way: usr_criteria[way]}).sort('new_pr')
	pos = 0
	for i in res:
		if i['name'] == name:
			break;
		else:
			pos += 1
	num = res.count()
	pos = num-pos
	return [pos+1, num+1] 

@mongo_collect
def rank_details(client, name):
	'''
	rank detail information.
	parameter:
		name
	return:
		x_data: scores's range
		world_data: name_id's rank information in the world
		friend_data: name_id's rank information in the first level
					 relationship
		mark: world: x_data[name_id], world_data[x_data]
			  friend: x_data[name_id], friend_data[x_data]
		max: [world, friend]
	'''
	# import pdb
	# pdb.set_trace()
	# use new_pr scores
	criteria = 'new_pr'
	### world info

	# get x_data, a list
	db = client.magnet.people
	tmp = db.find({criteria: {'$gt':0, '$lt':100}}).sort(criteria)
	x_data = []
	for i in tmp:
		tmp_i = round(i[criteria], 3)
		if tmp_i not in x_data:
			x_data.append(tmp_i)
	
	# get world_data, a list
	tmp = db.find({criteria: {'$gt':0, '$lt':100}}).sort(criteria)
	world_data = [0] * len(x_data)
	for i in tmp:
		for j in range(len(x_data)):
			if abs(x_data[j]-i['new_pr']) < 0.002:
				world_data[j] += 1
				break
	
	# get friend_data, a list
	db = client.magnet.links
	friends = db.find({'$or':[{'source': name}, {'target': name}]})
	friends_id = []
	for i in friends:
		friends_id.append(i['source'])
		friends_id.append(i['target'])
	friends_id = list(set(friends_id))

	db = client.magnet.people
	friends_score = []
	for i in db.find({'name':{'$in': friends_id}}):
		friends_score.append(i[criteria])

	friend_data = [0] * len(x_data)
	for i in friends_score:
		for j in range(len(x_data)):
			if abs(x_data[j]-i) < 0.002:
				friend_data[j] += 1
				break
	
	# get mark information
	my_score = db.find({'name': name})[0][criteria]
	mark = {}
	mark['world'] = [0, 0]
	mark['friend'] = [0, 0]
	temp_distinct = 100
	for i in x_data:
		if abs(my_score-i)<temp_distinct:
			temp_distinct = abs(my_score-i)
			mark['world'][0] = i
			mark['friend'][0] = i

	mark['world'][1] = world_data[x_data.index(mark['world'][0])]
	mark['friend'][1] = friend_data[x_data.index(mark['friend'][0])]

	# get max
	max_world_data = max(world_data)
	max_friend_data = max(friend_data)
	return dict(x_data = x_data, world_data = world_data,
				friend_data = friend_data, mark = mark, 
				max_data=max(max_friend_data, max_world_data))

if __name__ == '__main__':
	name = 'taotao.li'
	res = rank_details(name)
	print 'x_data :',  res['x_data']
	print 'world_data :',  res['world_data']
	print 'friend_data :',  res['friend_data']
	print 'mark :',  res['mark']