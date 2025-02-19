#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-19 15:40 
@file: initContextAcceptReceiveResult.py
@project: 5gAPItest
@describe: Powered By GW
"""
from message import *


def initContextAcceptReceiveAndResult(init_context_accept_message: bytes):

    # print(init_context_accept_message[26:28].hex())
    # print(init_context_accept_message[38:40].hex())

    init_context_response_message = InitialContextSetupResponse(
        amf_ue_ngap_id=init_context_accept_message[26:28].hex(),
        ran_ue_ngap_id=init_context_accept_message[38:40].hex(),
    )

    # print(init_context_response_message)

    return init_context_response_message.to_hex()


def test():
    # 示例数据
    init_context_accept_message = ("00044029000003000a0002000300550002000500260016157e03754327d7007e005d020204f0f0f0f0e1360102")
    print(f"init_context_accept_message: {init_context_accept_message}")
    # 拆分 NGAP 头部和 NAS-PDU
    init_context_response_message = initContextAcceptReceiveAndResult(bytes.fromhex(init_context_accept_message))

    # 打印结果
    print(f"init_context_response_message: {init_context_response_message}")


if __name__ == "__main__":
    test()
