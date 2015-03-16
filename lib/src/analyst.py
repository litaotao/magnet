# -*- coding: utf-8 -*-
from support import mongo_collect

@mongo_collect
def num_of_node_links(client):
	'''
	Get the number of people and relationships in total
	'''
	people = client.magnet.node.find().count()
	relationships = client.magnet.links.find().count()
	return people, relationships

@mongo_collect
def know_rate_me(client, user):
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
	db = client.magnet.links
	total = db.find({'target': user}).count()

	# get my new_score and rate_time
	db = client.magnet.people
	info = db.find({'name': user})[0]
	rate = len(info['people_rate_me'])
	new_score = info['new_pr']
	rate_time = info['ratetimes']

	return total, rate, new_score, rate_time

if __name__ == '__main__':
	people, relationships = num_of_node_links()
	print people
	print relationships
