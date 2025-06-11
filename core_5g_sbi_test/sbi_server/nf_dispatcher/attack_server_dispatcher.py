#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-04 17:49 
@file: attack_server_dispatcher.py
@project: 5gAPItest
@describe: Powered By GW
"""
from core_5g_sbi_test.core_sbi_messages.ausf import ausf_message_classes
from core_5g_sbi_test.core_sbi_messages.udm import udm_message_classes

import random


def random_dispatch():
    """
    随机从 UDM 消息类中选择一个类返回。
    可用于模拟测试或 fuzz 请求调度。
    """
    total_message_classes = ausf_message_classes + udm_message_classes
    if not total_message_classes:
        return None
    return random.choice(total_message_classes)


def random_dispatch_instance():
    """
    随机选择一个 UDM 消息类，并返回其实例（无 connection）。
    """
    total_message_classes = ausf_message_classes
    if not total_message_classes:
        return None
    cls = random.choice(total_message_classes)
    return cls(connection=None)
