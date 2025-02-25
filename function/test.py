#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-24 16:03 
@file: test.py
@project: 5gAPItest
@describe: Powered By GW
"""
from pycrate_mobile import *
from pycrate_corenet.Server import *

# 初始化服务器,serving 代表初始化服务器后立刻启动,Server代表服务端内容，
server = CorenetServer(threaded=True)

server.SERVER_GNB = {'INET'  : socket.AF_INET,
                  'IP'    : '127.0.0.1',
                  'port'  : 38412,
                  'MAXCLI': 16,
                  'errclo': True,
                  'GTPU'  : '127.0.0.1'}

auc = AuC.AUC_DB_PATH = f'../config/'

