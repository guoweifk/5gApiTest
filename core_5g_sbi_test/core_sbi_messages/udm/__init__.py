#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-03 11:15 
@file: __init__.py.py
@project: 5gAPItest
@describe: Powered By GW
"""
# udm/__init__.py
from .get_sm_data import GetSMDataProcessor
from .put_amf3gpp_access_registration import PutAmf3gppAccessRegistrationProcessor
from .get_smf_select_data import GetSmfSelectDataProcessor
from .get_am_data import GetAmDataProcessor
from .get_ueau_data import PostAuthDataProcessor

__all__ = ["GetSMDataProcessor", "PutAmf3gppAccessRegistrationProcessor", "GetSmfSelectDataProcessor",
           "GetAmDataProcessor", "PostAuthDataProcessor"]

# 所有消息类的集合
udm_message_classes = [
    GetSMDataProcessor,
    PutAmf3gppAccessRegistrationProcessor,
    GetSmfSelectDataProcessor,
    GetAmDataProcessor,
    PostAuthDataProcessor
]
