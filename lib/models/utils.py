# -*- coding: utf-8 -*-

"""
    utils.py
    ~~~~~~~~~~~~

    utilities for models use, some common used functions.

    :Author: taotao.li
    :last updated: May.18th.2014
"""

from flask import request, redirect
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
    profile = {age = 0, school = '', degree = '', gender = '', location = ''}
    resume = {field = [], hobby = [], skill = [], tag = []}
    relation = {ratetimes = 0, record = []} # record = [(), (),]

    if data:
        for i in data:
            profile[i] = data[i] if i in profile
            resume[i] = data[i] if i in resume
            relation[i] = data[i] if i in relation

    return dict(user = user, pwd = [pwd], profile = profile, ,
                resume = resume, relation = relation)
