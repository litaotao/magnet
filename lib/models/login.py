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
            dst_to, src_to = get_link_vector(name=user, level=1)
            nodes, links = build_links_nodes(dst_to, src_to)
            people, relationships = num_of_node_links()
            know_me, rate_me, new_score, rate_time = know_rate_me(user)
            data = get_profile(user = user)
            return Response(render_template('index.html',
                            server = str(server_addr)+':'+str(server_port),
                            user = user,
                            Number_1=people,
                            Number_2=relationships,
                            Number_3=know_me,
                            Number_4=rate_me,
                            rate_time=rate_time,
                            new_score=round(new_score,3)))
    
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


class Validate(Resource):
    """验证用户名是否可用"""        
    def post(self):
        user = request.form.get('user', '')
        # # validate user and pwd
        cursor = db['user'].find({'user': user}, {'pwd': 1, '_id': 1})
        #
        if cursor.count():
            return build_response(dict(code = -3, data = 'user already exist'))
        else:
            return build_response(dict(code = 200, data = 'user can be used'))

    def options(self):
        return build_response(dict(code = 200, data = ['POST, OPTIONS']))




