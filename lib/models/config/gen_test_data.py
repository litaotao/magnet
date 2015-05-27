# -*- coding: utf-8 -*-

"""
    gen_test_data.py
    ~~~~~~~~~~~~

    gen_test_data.py just genernate some test data to help me make magnet.

    :Author: taotao.li
    :last updated: Mar.26th.2015
"""

import json
from numpy.random import randint, rand

# self-defined package
from lib import server_addr, server_port, db
from lib.models import gen_user_context, print_func_name


@print_func_name
def gen_user(test_user_path):
    '''
    genernate test users from a file contains some test user name.
    '''
    data = json.load(file(test_user_path))
    db['user'].remove()
    for i in data:
        db['user'].insert(gen_user_context(i, '12345678', {'nickname': i.split('@')[0]}))

@print_func_name
def gen_link(test_user_path):
    '''
    genernate link.
    '''
    data = json.load(file(test_user_path))
    number = len(data)
    db['link'].remove()
    for i in range(number):
        for j in randint(0, number, randint(0, 10)):
            if i != j:
                db['link'].insert(dict(source = i, target = j, 
                                       weight = randint(1, 10)))

@print_func_name
def gen_node(test_user_path):
    '''
    genernate node.
    '''
    data = json.load(file(test_user_path))
    db['node'].remove()
    for i in data:
        db['node'].insert(dict(category=randint(1, 5), name=i, 
                               value=randint(1, 10)))



if __name__ == '__main__':
    # path = '/Users/chenshan/Desktop/user.txt'
    path = 'C:\\Users\\taotao.li\\Desktop\\user.txt'
    gen_user(path)
    gen_link(path)
    gen_node(path)



