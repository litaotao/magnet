# -*- coding: utf-8 -*-

"""
    server.py
    ~~~~~~~~~~~~

    Web Server API.

    :Author: taotao.li
    :last updated: Apr.13th.2015
"""


# official package
from flask import request, send_file, Response, render_template, redirect, g

# self-defined package
from . import app, api, admin_list

# import models for API interface
from models.login import Home, Login, Register



@app.after_request
def after(response):
    return response


@app.before_request
def before():
    pass


'''
# Restful API
'''
# home page
api.add_resource(Home, '/')
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')


# # 1
# @app.route('/', methods=['GET'])
# def home():
# 	###
# 	# from flask import flash
# 	# flash("this is a flash test")
# 	return Response(render_template('login.html',
# 									server=str(server_addr)+':'+str(server_port)))

# # 2
# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	# validate first
# 	if request.method == 'POST':
# 		try:
# 			user = request.form['user']
# 		except:
# 			user = 'username in POST'
# 		try:
# 			pwd = request.form['pwd']
# 		except:
# 			pwd = 'password in POST'
# 	else:
# 		return build_response(dict(data='Should be POST', code=-400))
# 	data, code = db_check(user, pwd)
# 	# validate succeed
# 	if code == 200:
# 		dst_to, src_to = get_link_vector(name=user, level=1)
# 		nodes, links = build_links_nodes(dst_to, src_to)
# 		people, relationships = num_of_node_links()
# 		know_me, rate_me, new_score, rate_time = know_rate_me(user)
# 		return Response(
# 					render_template('index.html',
# 									server=str(server_addr)+':'+str(server_port),
# 									user=user,
# 									Number_1=people,
# 									Number_2=relationships,
# 									Number_3=know_me,
# 									Number_4=rate_me,
# 									rate_time=rate_time,
# 									new_score=round(new_score,3)))
# 	else:
# 		return Response(
# 					render_template('login.html',
# 									error_msg=data,
# 									server=str(server_addr)+':'+str(server_port)))

# # 3
# @app.route('/classinfo', methods=['OPTIONS'])
# def get_classinfo_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 3
# @app.route('/classinfo', methods=['GET', 'POST'])
# def get_classinfo():
# 	'''
# 	return class info: field, skill, hobby, school to feed the
# 	select option in the front side
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		classinfo = get_class_info(info)
# 		res = dict(data=classinfo, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))	

# # 4
# @app.route('/similar', methods=['OPTIONS'])
# def filter_one_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 4
# @app.route('/similar', methods=['GET', 'POST'])
# def filter_one():
# 	'''
# 	traverse the database and find the first k most similar
# 	people to one.
# 	'''
# 	if request.method == 'GET':
# 		return build_response(dict(data='Should be POST', code=-400))
# 	else:
# 		criteria = request.json
# 	name = criteria['me']
# 	criteria.pop('me')
# 	data = filter_node_criteria(name, criteria, criteria.keys(), k=10)
# 	res = dict(data=data, code=200)
# 	return build_response(res)

# # 5
# @app.route('/validate', methods=['OPTIONS'])
# def validate_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 5
# @app.route('/validate', methods=['GET', 'POST'])
# def validate():
# 	if request.method == 'POST':
# 		try:
# 			user = request.form['user'].split('@')[0]
# 		except:
# 			user = 'username in POST'
# 		try:
# 			pwd = request.form['pwd']
# 		except:
# 			pwd = 'password in POST'
# 	else:
# 		return build_response(dict(data='Should be POST', code=-400))
# 	data, code = db_check(user, pwd)

# 	res = dict(data=data, code=code)
# 	return build_response(res)

# # 6
# @app.route('/rank', methods=['OPTIONS'])
# def rank_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 6
# @app.route('/rank', methods=['GET', 'POST'])
# def rank():
# 	'''
# 	return the rank result by rank_way
# 	rank_way_number - rank_way
# 	0 - place - location
# 	1 - age
# 	2 - gender
# 	3 - degree
# 	4 - skill
# 	5 - field
# 	6 - school
# 	'''
# 	if request.method == 'POST':
# 		rank_way = request.form['rank']
# 		name = request.form['user']
# 		rank_result = calculate_rank(name, int(rank_way))
# 		res = dict(data=rank_result, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))

# # 7
# @app.route('/details', methods=['OPTIONS'])
# def details_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 7
# @app.route('/details', methods=['POST', 'GET'])
# def details():
# 	'''
# 	return the details of ranking infomation by rank_way
# 	rank_way_number - rank_way
# 	0 - place - location
# 	1 - age
# 	2 - gender
# 	3 - degree
# 	4 - skill
# 	5 - field
# 	6 - school
# 	'''
# 	if request.method == 'POST':
# 		name = request.form['user']
# 		rank_result = rank_details(name)
# 		res = dict(data=rank_result, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))

# # 8
# @app.route('/update', methods=['OPTIONS'])
# def update_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 8
# @app.route('/update', methods=['POST', 'GET'])
# def update_info():
# 	'''
# 	server side for updated user information interface.
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		msg = update_user_info(info)
# 		res = dict(data=msg, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))	

# # 9
# @app.route('/user_info', methods=['OPTIONS'])
# def user_info_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 9
# @app.route('/user_info', methods=['GET', 'POST'])
# def user_info():
# 	'''
# 	get user info, fill the blanks in the user UI.
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		data = get_user_info(info)
# 		res = dict(data=data, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))	

# # 10
# @app.route('/friend_score', methods=['OPTIONS'])
# def friend_score_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 10
# @app.route('/friend_score', methods=['GET', 'POST'])
# def get_friend_score():
# 	'''
# 	Find the score and tag I ever tied to my friend
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		data = find_friend_score(info)
# 		res = dict(data=data, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))	

# # 11
# @app.route('/register', methods=['OPTIONS'])
# def register_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 11
# @app.route('/register', methods=['GET', 'POST'])
# def register():
# 	'''
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		msg = new_user(info)
# 		res = dict(data=msg, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))	

# # 12
# @app.route('/score_friend', methods=['OPTIONS'])
# def score_friend_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 12
# @app.route('/score_friend', methods=['GET', 'POST'])
# def score_friend():
# 	'''
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		msg = score_my_friend(info)
# 		res = dict(data=msg, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))

# # 13
# @app.route('/manage_friend', methods=['OPTIONS'])
# def manage_friend_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 13
# @app.route('/manage_friend', methods=['GET', 'POST'])
# def manage_friend():
# 	'''
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		msg = add_del_friend(info)
# 		res = dict(data=msg, code=200, msg=msg)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))

# # 14
# @app.route('/statistics', methods=['OPTIONS'])
# def statistics_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 14
# @app.route('/statistics', methods=['GET', 'POST'])
# def stat():
# 	'''
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		data = statistic(info, allow_user)
# 		res = dict(data=data, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))

# # 15
# @app.route('/vote', methods=['OPTIONS'])
# def vote_options():
# 	'''
# 	'''
# 	return build_response(dict())

# # 15
# @app.route('/vote', methods=['GET', 'POST'])
# def vote():
# 	'''
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		data = voting(info, vote_admin)
# 		res = dict(data=data, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))

# @app.route('/create_vote', methods=['OPTIONS'])
# def create_vote_options():
# 	'''
# 	'''
# 	return build_response(dict())

# @app.route('/create_vote', methods=['GET', 'POST'])
# def create_vote():
# 	'''
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		data = add_vote(info)
# 		res = dict(data=data, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))

# @app.route('/update_vote', methods=['OPTIONS'])
# def update_vote_options():
# 	'''
# 	'''
# 	return build_response(dict())

# @app.route('/update_vote', methods=['GET', 'POST'])
# def update_vote():
# 	'''
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		data = update_vote(info)
# 		res = dict(data=data, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))

# @app.route('/get_candidate', methods=['GET', 'POST'])
# def get_candidate():
# 	'''
# 	get candidate information when people click/change the candidate list.
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		data = get_candidate_info(info)
# 		res = dict(data=data, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))

# @app.route('/del_candidate', methods=['GET', 'POST'])
# def del_candidate():
# 	'''
# 	del a candidate.
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		data = remove_candidate(info)
# 		res = dict(data=data, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))

# @app.route('/score_candidate', methods=['GET', 'POST'])
# def score_candidate():
# 	'''
# 	score candidate API in vote module
# 	'''
# 	if request.method == 'POST':
# 		info = request.json
# 		data = give_score_candidate(info)
# 		res = dict(data=data, code=200)
# 		return build_response(res)
# 	else:
# 		print 'should be POST'
# 		return build_response(dict(data='Should be POST', code=-400))


# if __name__=='__main__':
# 	# test()
# 	# nodes,links = get_all()
# 	# print str(nodes).replace("\'","")
# 	# print str(links).replace("\'","")
# 	# client = MongoClient('localhost', 27017)
# 	app.run(host=server_addr, port=server_port, debug=True)


