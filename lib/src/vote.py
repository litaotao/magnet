# -*- coding: utf-8 -*-
from support import mongo_collect


@mongo_collect
def voting(client, info, vote_admin):
	'''
	code:
		0 --- there is no vote event
		1 --- there is a dominant vote event
	'''
	db = client.magnet.vote
	user = info['user']
	# if the user belongs to vote admin, he/she can create/delete/update a vote
	admin = 0
	if info['user'] in vote_admin:
		admin = 1
	# if there is no vote event
	if db.find().count() == 0:
		code = 0
		data = "there is no vote event, create one right now"
		res = dict(data=data, available=code, admin=admin)
		return res
	# if there is a current vote event
	# return the current and other votes' information
	else:
		code = 1
		data = get_full_vote(client)
		res = dict(data=data, available=code, admin=admin)
		return res


def get_full_vote(client):
	'''
	return vote information:
		vote_name --- string
		candidate: dict, key as candidate's name, value as a list, keys: score, desp
		winner: the first five people, a sorted list, [name, score] as  its member
	'''
	db = client.magnet.vote
	# get the current vote's information
	current = db.find({'current': True})[0]
	current_name = current['vote_name']
	current_candidate = current['candidate']
	current_candidate_name = current_candidate.keys()

	winner = []
	for i in current_candidate:
		winner.append([i, current_candidate[i]['total']])
	winner = sorted(winner, key=lambda d: d[1])
	current = dict(name=current_name, candidate=current_candidate, 
				   candidate_name=current_candidate_name, winner=winner)

	# get the vote's history information
	history = []
	for i in db.find({'current': False}):
		history.append(i['vote_name'])

	return dict(current=current, history=history)

@mongo_collect
def add_vote(client, info):
	'''
	add_new_vote = True, add a new vote, otherwise add a new candidate
	'''
	db = client.magnet.vote
	if info['add_new_vote']:
		db.insert({'vote_name': info['vote_name'],
				   'candidate': {},
				   'current': True})
		msg = 'Create a new vote: ' + info['vote_name'] + ' successfully'
	else:
		# import pdb
		# pdb.set_trace()
		candidate = db.find({'vote_name': info['vote_name']})[0]['candidate']
		c_name = info['candidate_name'].replace('.', '-') # c stands for candidate
		c_desp = info['candidate_description'] # desp stands for description
		c_score = {}
		c_total = 0
		candidate[c_name] = {}
		candidate[c_name]['desp'] = c_desp
		candidate[c_name]['score'] = c_score
		candidate[c_name]['total'] = c_total
		db.update({'vote_name': info['vote_name']}, 
					{'$set': {'candidate': candidate}
				 })
		msg = 'Add candidate: ' + c_name + ' for ' + info['vote_name'] + ' successfully'
	return msg

@mongo_collect
def update_vote(client, info):
	'''
	update a vote info
	there a two kinds of event to update a vote:
		1. just update a vote's name
		2. update a candidate's infomation: name, description, score
	'''
	db = client.magnet.vote
	if info['update_vote']:
		db.update({'vote_name': info['vote_name']},
					{'$set': {'vote_name': info['new_vote_name']}
				 })
		msg = 'update vote name successfully'
	elif info['update_score']:
		candidate = db.find({'vote_name': info['vote_name']})[0]['candidate']
		# mongo can't have a period . or a dollar sign $ in your field names
		# so if I insert candidate: {'taotao.li': {'desp': 'ddd', 'score': 0}}
		# for the '.' in 'taotao.li', mongo will raise an error:  not okForStorage
		c_name = info['candidate_name'].replace('.', '-')
		c_score = info['candidate_score']
		candidate[c_name]['score'] += c_score
		db.update({'vote_name': info['vote_name']},
					{'$set': {'candidate': candidate}
				 })
		# waiting test
		# db.update({'vote_name': info['vote_name']},
		# 			{'$inc': {'candidate['+c_name+'][score]': c_score}
		# 		  })
	elif info['update_desp']:
		candidate = db.find({'vote_name': info['vote_name']})[0]['candidate']
		c_desp = info['candidate_description']
		c_name = info['candidate_name']
		candidate[c_name]['desp'] = c_desp
		db.update({'vote_name': info['vote_name']},
					{'$set': {'candidate': candidate}
				  })
		msg = 'update ' + c_name + "'s description in " + info['vote_name']
	elif info['delete_candidate']:
		candidate = db.find({'vote_name': info['vote_name']})[0]['candidate']
		c_name = info['candidate_name']
		candidate.pop(c_name)
		db.update({'vote_name': info['vote_name']},
					{'$set': {'candidate': candidate}
				  })
		msg = 'Delete candidate ' + c_name + 'successfully'
	else:
		pass
	return msg

@mongo_collect
def get_candidate_info(client, info):
	'''
	get candidate information when people click/change the candidate list.
	return:
		candidate's total score, candidate's desp, candidate's score given by me
	'''
	# import pdb
	# pdb.set_trace()
	db = client.magnet.vote
	candidate = db.find({'vote_name':'new_vote'})[0]['candidate']
	candidate = candidate[info['user'].replace('.', '-')]
	# return candidate
	total = candidate['total']
	desp = candidate['desp']
	mine = candidate['score'].get(info['name'].replace('.', '-'), 0)

	return dict(total=str(total), desp=desp, mine=str(mine))

@mongo_collect
def remove_candidate(client, info):
	'''
	remove a candidate from database.
	'''
	db = client.magnet.vote
	candidate = db.find({'vote_name': info['vote']})[0]['candidate']
	candidate.pop(info['candidate_name'].replace('.', '-'))
	db.update({'vote_name': info['vote']}, {'$set': {'candidate': candidate}})

	msg = 'delete candidate:  ' + info['candidate_name'] + ' from ' + info['vote'] + ' successfully'
	return msg

@mongo_collect
def give_score_candidate(client, info):
	'''
	score candidate API in vote module
	'''
	# import pdb
	# pdb.set_trace()
	db = client.magnet.vote
	# import pdb
	# pdb.set_trace()
	candidate = db.find({'vote_name': info['vote']})[0]['candidate']
	old_score = candidate[info['candidate']]['score'].get(info['name'], 0)
	candidate[info['candidate']]['score'][info['name']] = float(info['score'])
	candidate[info['candidate']]['total'] += float(info['score'])
	candidate[info['candidate']]['total'] -= old_score
	db.update({'vote_name': info['vote']}, {'$set': {'candidate': candidate}})
	msg = 'vote candidate: ' + info['candidate'] + ' successfully'
	return msg


if __name__ == '__main__':
	# info = {"vote_name":"new_vote","candidate_name":"taotao.li","add_new_vote":0,"candidate_description":"dafsfaweasdf"}
	# msg = add_vote(info)
	# info = {"candidate":"kun-xue","vote":"new_vote","name":"taotao-li","score":"32"}
	# msg = give_score_candidate(info)
	# info = {"name":"taotao.li","user":"taotao.li","vote":"new_vote"}
	# msg = get_candidate_info(info)
	info = {"candidate":"siyuan-liu","vote":"new_vote","name":"taotao-li","score":"15"}
	mag = give_score_candidate(info)
	print msg

