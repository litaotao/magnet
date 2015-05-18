# -*- coding: utf-8 -*-
from support import mongo_collect


@mongo_collect
def db_check(client, user, pwd):
	'''
	Communicate with database to validate the username and password.
	return:
	valid:
		data: user's info
		code: 200
	unvalid:
		data: ''
		code: 400
	'''
	db = client.magnet.people
	temp = {}
	for i in db.find({'name': user}):
		temp[user] = i['pwd'][len(i['pwd'])-1]

	data = ''
	code = ''
	### this user does not exist in the database
	if not temp:
		data = 'user does not existed'
		code = -200
		return data, code
	### both user and pwd are valid
	elif temp[user] == pwd:
		data = 'valid user and password!'
		code = 200
		return data, code
	### user valid, but pwd not valid
	else:
		data = 'valid user, but invalid password'
		code = 201
		return data, code