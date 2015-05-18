# -*- coding: utf-8 -*-

"""
    login.py
    ~~~~~~~~~~~~

    login.py contains all the APIs to interact within the login page.

    :Author: taotao.li
    :last updated: Mar.18th.2015
"""

# official package
from flask import request, redirect
from flask.ext.restful import Resource
from flask import Flask, request, send_file, Response, render_template

# self-defined package
from lib import server_addr, server_port, db
from utils import build_response, gen_user_context


class Home(Resource):
    """主页"""
    def get(self):
        return Response(render_template('login.html',
                        server=str(server_addr)+':'+str(server_port)))

    def options(self):
        return build_response(dict(code=200, data=['GET, OPTIONS']))


class Login(Resource):
    """登陆"""
    def post(self):
        # import pdb; pdb.set_trace()
        user, pwd = request.form.get('user', ''), request.form.get('pwd', '')
        # # validate user and pwd
        cursor = db['user'].find({'user': user}, {'pwd': 1, '_id': 1})
        # 
        if not cursor.count():
            return build_response(dict(code = -1, data = 'user not exist'))
        elif cursor[0].get('pwd', [])[-1] != pwd:
            return build_response(dict(code = -2, data = 'password not validate'))
        else:
            return build_response(dict(code = 200, data = 'success'))
    
    def options(self):
        return build_response(dict(code = 200, data = ['POST, OPTIONS']))


class Register(Resource):
    """注册"""        
    def post(self):
        # import pdb; pdb.set_trace()
        user, pwd = request.json.get('user', ''), request.json.get('pwd', '')
        # # validate user and pwd
        cursor = db['user'].find({'user': user}, {'pwd': 1, '_id': 1})
        #
        if cursor.count():
            return build_response(dict(code = -3, data = 'user already exist'))
        else:
            data = gen_user_context(user, pwd)
            db['user'].insert(data)
            data.pop('_id')   ###  it's so funny, data会被insert函数改变的，回头看看insert源码
            data.pop('pwd')
        return build_response(dict(code = 200, data = data))

    def options(self):
        return build_response(dict(code = 200, data = ['POST, OPTIONS']))


