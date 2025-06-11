#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-04 19:46 
@file: ausf_server_dispatcher.py
@project: 5gAPItest
@describe: Powered By GW
"""
from core_5g_sbi_test.core_sbi_messages.ausf import ausf_message_classes

def dispatch(path: str):
    """
    遍历 UDM 消息类，匹配并处理该 path 请求。
    返回 True 表示已处理，False 表示未匹配。
    """
    for cls in ausf_message_classes:
        handler = cls(connection=None)  # 接收时不需要 connection
        if handler.match(path):
            return cls
    return None