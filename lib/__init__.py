# -*- coding: utf-8 -*-

"""
    __init__.py
    ~~~~~~~~~~~~

    Initial all context in this file. Configure file read, and database connection.
    Should stress that we should import server.py in the last, then when files/modules
    changed which are imported in server.py, the app will reload automatically when 
    app.Debug is True.

    :Author: taotao.li
    :last updated: Mar.18th.2015
"""

import ConfigParser
from pymongo import MongoClient
from flask import Flask
from flask.ext.restful import Api


cf = ConfigParser.ConfigParser()
cf.read('etc/magnet.conf')
if not cf.has_section('server'):
    cf.read('../etc/magnet.conf')
if not cf.has_section('server'):
    cf.read('../../etc/magnet.conf')
if not cf.has_section('server'):
    cf.read('../../../etc/magnet.conf')
if not cf.has_section('server'):
    cf.read('../../../../etc/magnet.conf')

## app server
server_addr = cf.get('server', 'server_addr')
server_port = cf.get('server', 'server_port')


## mongo server
mongo_host = cf.get('mongo', 'mongo_host')
mongo_port = cf.get('mongo', 'mongo_port')
local_test = cf.get('mongo', 'local_test')


##
admin_list = cf.get('admin', 'users')
admin_list = admin_list.replace(' ', '').split(';')


if local_test.upper() == 'TRUE':
    mongo_client = MongoClient(host=mongo_host, port=int(mongo_port))
else:
    mongo_client = MongoClient(host=mongo_host, port=int(mongo_port))
    try:
        mongo_client.community.authenticate(mongo_user, mongo_pass)
    except:
        error.error('mongodb connect or authenticate failed')

## init database map
db = dict(link = mongo_client.magnet2.link, user = mongo_client.magnet2.user,
          node = mongo_client.magnet2.node, vote = mongo_client.magnet2.vote)

## init flask app
app = Flask(__name__, static_url_path='/static', static_folder='static',)
app.secret_key = "wow, this girl send a ^_^ to me, what does that mean?"
api = Api(app)


import server

