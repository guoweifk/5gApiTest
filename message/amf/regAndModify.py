#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-05-06 21:40 
@file: regAndModify.py
@project: 5gAPItest
@describe: Powered By GW
"""
import tosmfmodify
import regtosm
import release
import time


n2SmInfoType = ["NULL", "PDU_RES_SETUP_REQ", "PDU_RES_SETUP_RSP", "PDU_RES_SETUP_FAIL", "PDU_RES_REL_CMD", "PDU_RES_REL_RSP", "PDU_RES_MOD_REQ", "PDU_RES_MOD_RSP", "PDU_RES_MOD_FAIL", "PDU_RES_NTY", "PDU_RES_NTY_REL", "PDU_RES_MOD_IND", "PDU_RES_MOD_CFM", "PATH_SWITCH_REQ", "PATH_SWITCH_SETUP_FAIL", "PATH_SWITCH_REQ_ACK", "PATH_SWITCH_REQ_FAIL", "HANDOVER_REQUIRED", "HANDOVER_CMD", "HANDOVER_PREP_FAIL", "HANDOVER_REQ_ACK", "HANDOVER_RES_ALLOC_FAIL", "SECONDARY_RAT_USAGE", "PDU_RES_MOD_IND_FAIL", "UE_CONTEXT_RESUME_REQ", "UE_CONTEXT_RESUME_RSP", "UE_CONTEXT_SUSPEND_REQ"]

for i in range(1000):
    result = regtosm.send_http2_request()
    # result =101
    print(result)
    # print (n2SmInfoType[5])
    time.sleep(1)
    tosmfmodify.send_http2_modify(result-1, n2SmInfoType[5])
    release.send_http2_release(result)
    release.send_http2_release(result - 8)
    release.send_http2_release(result - 7)
    release.send_http2_release(result - 6)
    release.send_http2_release(result - 5)
    release.send_http2_release(result - 4)
    release.send_http2_release(result - 3)
    release.send_http2_release(result-2)
    release.send_http2_release(result - 1)
    release.send_http2_release(result + 1)
    release.send_http2_release(result + 2)
    release.send_http2_release(result + 3,)
    release.send_http2_release(result + 4)
    release.send_http2_release(result + 5)
    release.send_http2_release(result + 6)
