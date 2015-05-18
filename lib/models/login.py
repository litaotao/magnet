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
from lib import server_addr, server_port
from utils import build_response


class Home(Resource):
    """主页"""
    def get(self):
        return Response(render_template('login.html',
                        server=str(server_addr)+':'+str(server_port)))

    def options(self):
        return build_response(dict(code=200, data=['GET, OPTIONS']))


class Login(Resource):
    """登陆"""
    def get(self):
        return build_response(dict(code=200, data='get'))
        
    def post(self):
        return build_response(dict(code=200, data='post'))
    
    def put(self):
        return build_response(dict(code=200, data='put'))
        
    def delete(self):
        return build_response(dict(code=200, data='delete'))

    def options(self):
        return build_response(dict(code=200, data='welcome'))


class Register(Resource):
    """注册"""
    def get(self):
        return build_response(dict(code=200, data='get'))
        
    def post(self):
        return build_response(dict(code=200, data='post'))
    
    def put(self):
        return build_response(dict(code=200, data='put'))
        
    def delete(self):
        return build_response(dict(code=200, data='delete'))

    def options(self):
        return build_response(dict(code=200, data='welcome'))


