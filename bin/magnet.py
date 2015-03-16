#coding=utf-8
# -*- coding: utf-8 -*-
"""
	magnet.py
	~~~~~~~~~~~~

	web interface, using flask and restful

	:copyright: (c) 2014 by DataYes Fixed Income Team.
	:Author: taotao.li
	:last updated: Aug.19rd.2014
"""

import sys
sys.path.insert(0,'../')
sys.path.insert(0,'../lib')

from lib.server import app

if __name__ == '__main__':
	app.run(host = '127.0.0.1', port = 5000, debug = True)