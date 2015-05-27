# -*- coding: utf-8 -*-

"""
    profile.py
    ~~~~~~~~~~~~

    Contains all the API about geting people's personal data in their main page.

    :Author: taotao.li
    :last updated: Mar.21st.2015
"""

# official package
from flask import request, redirect
from flask.ext.restful import Resource
from flask import Flask, request, send_file, Response, render_template


from utils import build_response
from analyst import calculate_rank


class Rank(Resource):
    """用户排名信息"""
    def get(self, rank_by, nickname):
        '''
        获取user的排名
        '''
        res = calculate_rank(nickname, rank_by)
        return build_response(dict(code = 200, data = res))

    def options(self):
        return build_response(dict(code = 200, data = ['GET, OPTIONS']))






