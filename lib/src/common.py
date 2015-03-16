# -*- coding: utf-8 -*-
from support import mongo_collect
from prank import calc_new_pr
from flask import make_response, jsonify
from operator import isNumberType

# @log_func(logging)
@mongo_collect
def get_link_vector(client, name, level=0):
	'''
	get link vector of name in level hirachy
	this is the mid-function for build nodes and links
	parameters:
		name : user name
		level: the hierachy level to traverse
	return:
		src_to:
		dst_to:
	'''
	db = client.magnet.links
	dst_to = []		# store the vector of links from name to others
					# will use this to construct nodes and links
	src_to = []		# store the vector of links from others to name

	if level<1:
		return [], []

	db = client.magnet.links
	for i in db.find({'source': name}):
		dst_to.append([str(i['source']), str(i['target'])])
	for i in db.find({'target': name}):
		src_to.append([str(i['source']), str(i['target'])])

	# find all the vector from name to others in hierachy
	# import pdb
	# pdb.set_trace()
	current=[]
	for k in range(1, level):
		temp = [i[1] for i in dst_to]
		if current:
			temp = [i[1] for i in current]
			current = []
		for name in temp:
			for i in db.find({'source': name}):
				current.append([str(i['source']), str(i['target'])])

		dst_to.extend(current)
	
	# find all the vectore from others to name in hierachy
	current=[]
	for k in range(1, level):
		temp = [i[0] for i in src_to]
		if current:
			temp = [i[0] for i in current]
			current = []
		for name in temp:
			for i in db.find({'target': name}):
				current.append([str(i['source']), str(i['target'])])
				
		src_to.extend(current)

	return dst_to, src_to

# @log_func(logging)
@mongo_collect
def build_links_nodes(client, dst_to, src_to):
	'''
	use the return of get_link_vector to build nodes and links
	of one people in hierachy level
	parameters:
		dst_to:
		src_to:
	return:
		nodes:
		links:
	'''
	db = client.magnet.node
	
	### firstly we should find all the people node that should be returned
	temp = []
	for i in dst_to:
		temp.extend(i)
	for i in src_to:
		temp.extend(i)
	temp = set(temp)

	### build nodes from dst_to and src_to
	# import pdb
	# pdb.set_trace()
	nodes = []
	for i in temp:
		temp_node = db.find({'name': i},{'_id': 0})
		if temp_node.count():
			nodes.append(temp_node[0])

	### build links from dst_to and src_to
	db = client.magnet.links
	links = []
	for i in dst_to:
		temp_link = db.find({'source': i[0], 'target': i[1]},{'_id': 0})
		if temp_link.count():
			links.append(temp_link[0])
	for i in src_to:
		temp_link = db.find({'source': i[0], 'target': i[1]},{'_id': 0})
		if temp_link.count():
			links.append(temp_link[0])

	return nodes, links

@mongo_collect
def get_class_info(client, user):
	'''
	return class info: field, skill, hobby, school to feed the
	select option in the front side
	comment:
		this need refactor these two days, need new hobby,school,field,skill
		data to feed
	parameters: 
		user: user name
	return:

	'''
	db = client.magnet.people
	res = {}
	info = ['field', 'skill', 'hobby', 'school']
	tmp_res = {}
	tmp_hobby = []
	tmp_school = []

	for i in db.find():
		# get the hobby and school list
		if type(i['hobby']) == list:
			tmp_hobby.extend(i['hobby'])
		else:
			tmp_hobby.append(i['hobby'])
		if type(i['school']) == list:
			tmp_school.extend(i['school'])
		else:
			tmp_school.append(i['school'])

		temp = i['skill']
		if temp:
			field = temp[0].split('-')[0]
		else:
			continue

		if field and field in tmp_res:
			# the tmp_res[current skill] is not empty
			if tmp_res[field]:
				tmp_res[field].extend(temp)
			else:
				tmp_res[field] = []
		elif field:
			tmp_res[field] = list(temp)
		else:
			pass

	# set the skills of one field unique
	for i in tmp_res.keys():
		tmp_res[i] = list(set(tmp_res[i]))
	res['field'] = tmp_res
	res['field_name'] = tmp_res.keys()
	res['hobby'] = list(set(tmp_hobby))
	res['school'] = list(set(tmp_school))

	# judge whether the user update password or not
	name = user['name']
	pwd = db.find({'name': name})[0]['pwd']
	if len(pwd)==1 or pwd[len(pwd)-1] == '12345678':
		res['first_time'] = True;
	else:
		res['first_time'] = False;

	# return relationships of people
	dst_to, src_to = get_link_vector(name=name, level=1)
	nodes, links = build_links_nodes(dst_to, src_to)
	res['nodes'] = nodes
	res['links'] = links

	return res

@mongo_collect
def update_user_info(client, info):
	'''
	info should contains only the msg whcih really need updated.
	thus if info[key] is none or null or anything invalid else, weight
	should first remove this key-value pair in the info;
	parameters:
		info: 
	'''
	db = client.magnet.people
	name = info['name']
	info.pop('name')

	for i in info.keys():
		if i=='pwd':
			db.update({'name': name},
						{'$push':
							{'pwd': info[i]}
					    })
		else:
			db.update({'name': name},
						{'$set':
							{i: info[i]}
						})
	return 'Your personal info has been updated successfully!'

@mongo_collect
def get_user_info(client, info):
	'''
	get user info, fill the blanks in the user UI.
	'''
	# basic info
	name = info['name']

	db = client.magnet.people
	basic = db.find({'name': name}, {'_id': 0, 'new_pr': 0, 'origin_pr': 0})[0]

	# friend info
	friend = []
	db = client.magnet.links
	for i in db.find({'source': name}):
		friend.append(i['target'])

	return dict(basic=basic, friend=friend)

@mongo_collect
def find_friend_score(client, info):
	'''
	Find the score and tag I ever tied to my friend
	'''
	db = client.magnet.links
	return db.find({'source': info['me'], 'target': info['friend']})[0]['weight']

@mongo_collect
def new_user(client, info):
	'''
	'''
	db = client.magnet.people
	db.insert({'name': info['name'], 'pwd': [info['pwd']],
				'age': 'empty', 'degree': 'empty',
				'field': 'empty', 'gender': 'empty',
				'hobby': 'empty', 'skill': 'empty',
				'location': 'empty', 'new_pr': 0,
				'origin_pr': 0, 'school': 'empty',
				'people_rate_me': [], 'tag': [],
				'ratetimes': 0})
	db = client.magnet.node
	db.insert({'name': info['name'], 'category': 3, 'value': 5})
	return 'user register successfully!'

@mongo_collect
def score_my_friend(client, info):
	'''
	give your friend a score and tag him;
	'''
	db = client.magnet.links
	db.update({'source': info['my'], 'target': info['friend']},
				{'$set':
					{'weight': float(info['score'])}
				})

	db = client.magnet.people
	origin_tag = db.find({'name': info['friend']})[0]['tag']
	origin_tag.extend(info['tag'])
	
	# when a friend has just been scored, his personal pr should be
	# recalculated once again.
	calc_new_pr(info['friend'])

	# should preprocess origin_tag before updating into database
	# here we just remove the repeated items
	origin_tag = list(set(origin_tag))
	people_rate_me = db.find({'name': info['friend']})[0]['people_rate_me']
	people_rate_me.append(info['my'])
	people_rate_me = list(set(people_rate_me))

	db.update({'name': info['friend']},
				{'$set':
				{'people_rate_me': people_rate_me}
			 })
	db.update({'name': info['friend']},
				{'$set':
					{'tag': origin_tag}
			 })
	db.update({'name': info['friend']},
				{'$inc': {'ratetimes':1}
			 })

	return "update your score and comment to your friend successfully"
	
@mongo_collect
def add_del_friend(client, info):
	'''
	friend relationship management; on account of the lack of preprocessing
	in the front side, we need to first validate the name people want to 
	add or delete.
	'''
	# firstly, check whether it is valid the people we want to add or delete
	# or not
	db = client.magnet.people
	if not db.find({'name': info['friend']}).count():
		return 'Opps, the friend \'' + info['friend'] + '\' you want to add \
		or delete still not sign up in Magnet'

	db = client.magnet.links
	if info['method'] == 'add':

		db.insert({'source': info['me'], 'target': info['friend'],
					'weight': 5})
		return 'add friend: ' + info['friend'] + ' successfully'
	else:
		db.remove({'source': info['me'], 'target': info['friend']})
		return 'del friend: ' + info['friend'] + ' successfully'

@mongo_collect
def statistic(client, info, allow_user):
	'''
	just return the first 20 people whose score is the best.
	'''
	db = client.magnet.people
	user = info['user']
	data = [[],[]]
	if user in allow_user or 'unlimited' in allow_user:
		for i in db.find({},{'name':1,'new_pr':1}).sort([('new_pr',-1)]).limit(20):
			data[0].append(i['name'])
			data[1].append(round(i['new_pr'],3))
		available = 1
	else:
		available = 0
		data = ""
	
	return dict(data=data, available=available)

def build_response(content):
    response = make_response( jsonify(content) )
    # set response headers.
    response.headers['Access-Control-Allow-Methods'] = 'PUT, POST, GET, OPTIONS, DELETE, PATCH'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = \
            'Origin, X-Requested-With, Content-Type, Accept, Authorization'

    return response


if __name__ == '__main__':
	# test get_class_info
	# class_info = get_class_info({'name':'taotao.li'})
	# print 'class_info   ', class_info
	# test(5,6,7,k='key')
	dst_to, src_to = get_link_vector('taotao.li', level=2)
	print 'dst_to  ', len(dst_to), dst_to
	print 'src_to  ', len(src_to), src_to
	nodes, links = build_links_nodes(dst_to, src_to)
	print 'nodes   ', nodes
	# print 'links   ', links
	# nodes, links = get_all()
	# print 'nodes   ', nodes
	# print 'links   ', links
	# score = get_score(4, 14)
	# print 'score   ', score
	# set_score(4, 14, 10)
	# score = get_score(4, 14)
	# print 'score   ', score
	pass