# -*- coding: utf-8 -*-

"""
    gen_test_data.py
    ~~~~~~~~~~~~

    gen_test_data.py just genernate some test data to help me make magnet.

    :Author: taotao.li
    :last updated: Mar.26th.2015
"""

import json

# self-defined package
from lib import server_addr, server_port, db
from models import gen_user_context, print_func_name


@print_func_name
def gen_user(path):
	'''
	genernate test users from a file contains some test user name.
	'''
	data = json.load(file(path))
	for i in data:
		db['user'].insert(gen_user_context(i))





if __name__ == '__main__':
	gen_user()



