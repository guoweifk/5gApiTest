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
from .ngap.ngapSplit import split_ngap_nas
from .ngap.ngapDownLinkNASTransport import NGAPDownLinkTransportNASMessage

# 从 nas 里导入关键方法
from .nas.authrequestMessage import AuthenticationRequestMessage
from .nas.authresponseMessage import AuthenticationResponseMessage

# 让 message 直接使用这些方法
__all__ = ["split_ngap_nas", "NGAPDownLinkTransportNASMessage", "AuthenticationRequestMessage", "AuthenticationResponseMessage"]
