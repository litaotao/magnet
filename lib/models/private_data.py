# -*- coding: utf-8 -*-

"""
    private_data.py
    ~~~~~~~~~~~~

    private_data.py contains all the APIs to get one's info.

    :Author: taotao.li
    :last updated: Mar.26th.2015
"""


def know_rate_me(user):
	'''
	Get the total number of people who knows me and the number
	of people who rated me.
	parameters:
		user: user name
	return:
		total: the total number of people who knows me
		rate:  the total number of people who rates me
		new_score: my current score
		rate_time: the total number of times people rate me
	'''
	# get know_me and rate_me
	total_know_me = db['link'].find({'target': user}).count()

	# get my new_score and rate_time
	cursor = db['user'].find({'user': user})
	if not cursor.count():
		return 0, 0, 0, 0

	relation = cursor[0].get('relation', {})
	rate_me = len(relation.get('record', []))
	new_score = relation.get('new_score', 0)

	return total_know_me, rate_me, new_score, rate_time