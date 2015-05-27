# -*- coding: utf-8 -*-

"""
    utils.py
    ~~~~~~~~~~~~

    utilities for models use, some common used functions.

    :Author: taotao.li
    :last updated: May.18th.2014
"""

from flask import request, redirect
from numpy.random import randint, rand
from functools import wraps
from flask import make_response, jsonify, Response
from lib import admin_list
import json 


def build_response(content, code=200):
    """Build response, add headers"""
    response = make_response( jsonify(content), content['code'] )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = \
            'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    return response

def gen_user_context(user, pwd, data = None):
    """Build an user context for a new user""" 
    profile = dict(age = str(randint(18, 50)), school = '', degree = '', gender = '', location = '', nickname = '')
    resume = dict(field = '', hobby = '', skill = '', tag = '')
    relation = dict(record = [], new_score = 0) # record = [(), (),]

    if data:
        for i in data:
            profile[i] = data[i] if i in profile else None
            resume[i] = data[i] if i in resume else None
            relation[i] = data[i] if i in relation else None

    return dict(user = user, pwd = [pwd], profile = profile,
                resume = resume, relation = relation)

'''
# A simple wrapper, print func name when been executed.
'''
def print_func_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print 'start execute {} ...'.format(func.__name__)
        result = func(*args, **kwargs)
        print 'end execute {} ...\n----------'.format(func.__name__)
        return result
    return wrapper

