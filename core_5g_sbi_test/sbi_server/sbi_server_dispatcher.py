#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-04 15:00 
@file: sbi_server_dispatcher.py
@project: 5gAPItest
@describe: Powered By GW
"""
from core_5g_sbi_test.sbi_server.nf_dispatcher import smf_server_dispatcher, amf_server_dispatcher, \
    udm_server_dispatcher, attack_server_dispatcher,ausf_server_dispatcher

START_ATTACK = True
NF_DISPATCH_TABLE = {
    # "SMF": smf_server_dispatcher.dispatch,
    # "AMF": amf_server_dispatcher.dispatch,
    "UDM": udm_server_dispatcher.dispatch,
    "AUSF": ausf_server_dispatcher.dispatch
    # 其他 NF 可继续扩展
}


def dispatch(path: str, headers: dict):
    user_agent = headers.get("user-agent", "").upper()
    print(f"user-agent {user_agent}")
    ## 注入攻击
    if START_ATTACK:
        return attack_server_dispatcher.random_dispatch_instance()

    nf_dispatch = NF_DISPATCH_TABLE.get(user_agent)
    if nf_dispatch:
        return nf_dispatch(path)
    return None
