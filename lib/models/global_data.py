# -*- coding: utf-8 -*-

"""
    global_data.py
    ~~~~~~~~~~~~

    global_data.py contains all the APIs to get the global info.

    :Author: taotao.li
    :last updated: Mar.26th.2015
"""

# self-defined package
from lib import server_addr, server_port, db


def get_total_user_relation():
	'''
	获取当前所有用户的关系数量.
	'''
	t_people = db['node'].find().count()
	t_relationships = db['link'].find().count()

	return t_people, t_relationships




