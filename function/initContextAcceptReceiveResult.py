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
    print(init_context_accept_message[26:28].hex())
    print(init_context_accept_message[38:40].hex())

    init_context_response_message = InitialContextSetupResponse(
        amf_ue_ngap_id=init_context_accept_message[26:28].hex(),
        ran_ue_ngap_id=init_context_accept_message[38:40].hex(),
    )

    print(init_context_response_message)

    return init_context_response_message.to_hex()


def test():
    # 示例数据
    init_context_accept_message = (
                "000e008090000008000a00020002005500020001001c00070000f110020040000000020001007700091c0"
                + "00e000700038000005e0020ed3f02cf6478ce929dadc5853d351716aee89887b473602385ffeee2f0389"
                + "bce002240084370816125ffff510026402f2e7e023d4210c9017e0042010177000bf200f110020040f40"
                + "0303e54072000f11000000115020101210201005e01a9")
    print(f"init_context_accept_message: {init_context_accept_message}")
    # 拆分 NGAP 头部和 NAS-PDU
    init_context_response_message = initContextAcceptReceiveAndResult(bytes.fromhex(init_context_accept_message))

    # 打印结果
    print(f"init_context_response_message: {init_context_response_message}")


if __name__ == "__main__":
    test()
