# -*- coding: utf-8 -*-

"""
    analyst.py
    ~~~~~~~~~~~~

    Contains all the functions about calculating one's kinds of info.

    :Author: taotao.li
    :last updated: Mar.27th.2015
"""


# self-defined package
from lib import server_addr, server_port, db


def calculate_rank(nickname, rank_by):
    '''
    return the rank result by rank_way
    rank_by: place, age, gender, degree, skill, field, school
    '''
    # import pdb; pdb.set_trace()
    profile = dict(age = 0, school = '', degree = '', gender = '', location = '', nickname = '')
    resume = dict(field = '', hobby = '', skill = '', tag = '')

    if rank_by not in profile and rank_by not in resume:
        return [0, 0]

    #
    tmp = db['user'].find({'profile.nickname': nickname}, {'_id': 0, 'profile': 1, 'resume': 1})[0]
    dsl = ''
    if rank_by in profile:
        dsl = {'profile.' + rank_by : tmp['profile'].get(rank_by, '')}
    elif rank_by in resume:
        dsl = {'resume.' + rank_by : '/*{}*/'.format(tmp['resume'].get(rank_by, ''))}

    dsl2 = {'user': 1, '_id': 0, 'relation': 1, 'profile': 1}
    cursor = db['user'].find(dsl, dsl2).sort('relation.new_score')

    tmp = list(cursor)
    index = tmp.index([i for i in tmp if i['profile']['nickname'] == nickname].pop())

    return [len(tmp), index]

