#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-18 19:42 
@file: __init__.py.py
@project: 5gAPItest
@describe: Powered By GW
"""
# 从 ngap 里导入关键方法
from message.ngap import split_ngap_nas
from message.ngap import NGAPDownLinkTransportNASMessage
from message.ngap import NGAPUplinkTransportNASMessage
from message.ngap import InitialContextSetupResponse
# 从 nas 里导入关键方法
from message.nas import AuthenticationRequestMessage
from message.nas import AuthenticationResponseMessage


import os
import sys

# 获取当前 message 目录的绝对路径
message_path = os.path.dirname(os.path.abspath(__file__))

# 确保 function 目录在 sys.path 里
if message_path not in sys.path:
    sys.path.append(message_path)

# 自动导入 function 目录下的所有 Python 文件（去掉 __init__.py）
for module in os.listdir(message_path):
    if module.endswith(".py") and module != "__init__.py":
        module_name = module[:-3]  # 去掉 ".py"
        __import__(f"message.{module_name}")

# 让 message 直接使用这些方法
__all__ = ["split_ngap_nas", "NGAPDownLinkTransportNASMessage", "NGAPUplinkTransportNASMessage","AuthenticationRequestMessage",
           "AuthenticationResponseMessage","InitialContextSetupResponse"]
