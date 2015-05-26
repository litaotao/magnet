# -*- coding: utf-8 -*-

"""
    profile.py
    ~~~~~~~~~~~~

    Contains all the API about geting people's personal data in their main page.

    :Author: taotao.li
    :last updated: Mar.21st.2015
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
    total = db['link'].find({'target': user}).count()

    # get my new_score and rate_time
    info = db['people'].find({'name': user})[0]
    rate = len(info['people_rate_me'])
    new_score = info['new_pr']
    rate_time = info['ratetimes']

    return dict(total = total, rate = rate, new_score = new_score, 
                rate_time = rate_time)





