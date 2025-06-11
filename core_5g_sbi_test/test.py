#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-03 23:00 
@file: test.py
@project: 5gAPItest
@describe: Powered By GW
"""
# import SBIConnection,SBIProcessor
from core_5g_sbi_test.core_sbi_messages import *
from core_5g_sbi_test.sbi_client import *

processor = SBIClientProcessor(SBIConnection("127.0.0.12", 7777))
processor.add_step(GetSmfSelectDataProcessor)
processor.add_step(PutAmf3gppAccessRegistrationProcessor)
processor.add_step(GetSMDataProcessor)
processor.run()