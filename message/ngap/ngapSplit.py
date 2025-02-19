#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-18 19:51
@file: ngapSplit.py
@project: 5gAPItest
@describe: Powered By GW
"""


def split_ngap_nas(message: str):
    """
    拆分 NGAP 消息为 NGAP 头部和 NAS-PDU（不解析具体字段）

    :param message: 16 进制字符串的完整 NGAP 消息
    :return: (ngap_header, nas_pdu) 分别为 NGAP 头部和 NAS-PDU
    """
    message = message.upper()  # 统一大写，确保格式一致

    # NAS-PDU 长度字段的位置（前 4 位用于标识其长度）
    nas_pdu_length_start = 24 * 2  # 24 字节（长度字段之前的数据）

    # 拆分 NGAP 头部（包含 NAS-PDU 长度字段）
    ngap_header = message[:nas_pdu_length_start]

    # 拆分 NAS-PDU
    nas_pdu = message[nas_pdu_length_start:]

    return ngap_header, nas_pdu

def test():
    # 示例数据
    auth_down_message_hex = "0004403e000003000a000200020055000200010026002b2a7e005601020000216b0bbf58144c8d74ade24b5626bd5d2f2010719762a4686f80005ec4e5f58c90a204"
    auth_up_message_hex = "002E4040000004000A0002000200550002000100260016157E00572D106A9EF8FC9D2C11A36D4DA18229C3B925007940135000F110000000010000F110000001EB5DA5BA"

    security_down_message_hex = "00044029000003000a0002000200550002000100260016157e034789381d007e005d020104f0f0f0f0e1360102"
    security_up_message_hex = "002e4067000004000a000200020055000200010026003d3c7e04f15f1642007e005e7700094573806121856151f17100237e004179000d0100f1100000000000000000001001002e04f0f0f0f02f020101530100007940135000f110000000010000f110000001eb5da5ba"
    "002e4067000004000a000200020055000200010026003d3c7e04f15f1642007e005e7700094573806121856151f17100237e004179000d0100f1100000000000000000001001002e04f0f0f0f02f020101530100007940135000f110000000010000f110000001eb5da5ba"
    "002E4040000004000A0002000200550002000100260016157E00572D106A9EF8FC9D2C11A36D4DA18229C3B925007940135000F110000000010000F110000001EB5DA5BA"
    # 拆分 NGAP 头部和 NAS-PDU
    ngap_header, nas_pdu = split_ngap_nas(auth_down_message_hex)

    # 打印结果
    print(f"NGAP Header: {ngap_header}")
    print(f"NAS-PDU: {nas_pdu}")


if __name__ == "__main__":
    test()
