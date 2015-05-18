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