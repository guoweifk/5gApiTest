#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-05-05 16:25 
@file: __init__.py.py
@project: 5gAPItest
@describe: Powered By GW
"""
from .post_ue_au_data import PostUeAuthenticationProcessor
from .put_5g_aka_conf_processor import Put5gAkaConfirmationProcessor

__all__ = ["PostUeAuthenticationProcessor", "Put5gAkaConfirmationProcessor"]

# 所有消息类的集合
ausf_message_classes = [
    PostUeAuthenticationProcessor,
    Put5gAkaConfirmationProcessor
]
