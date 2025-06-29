#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-18 20:16 
@file: authReceiveResult.py
@project: 5gAPItest
@describe: Powered By GW
"""
from message import *
from utils import *
import time

def authReceiveAndResult(auth_request:bytes):
    ngap_header, nas_pdu = split_ngap_nas(auth_request)
    ngap_downlink_message = NGAPDownLinkTransportNASMessage.parse(ngap_header)
    authentication_request_message = AuthenticationRequestMessage.parse(nas_pdu)
    # print(ngap_downlink_message)
    # print(authentication_request_message)
    current_timestamp = int(time.time())

    # 转换为十六进制格式（大写）
    hex_timestamp = format(current_timestamp, 'X')
    ngap_uplink_message = NGAPUplinkTransportNASMessage(
        amf_ue_ngap_id=ngap_downlink_message.amf_ue_ngap_id,
        ran_ue_ngap_id=ngap_downlink_message.ran_ue_ngap_id,
        ngap_message_len= "40",
        nas_pdu_type= "0016",
        nas_pdu_length="15"
    )
    KSEAF,res_star = calculateRes(bytes.fromhex(authentication_request_message.rand),bytes.fromhex(authentication_request_message.sqn_xor_ak))
    # print(f"res_star: {res_star}")
    authentication_response_message = AuthenticationResponseMessage(
        res_star= res_star,
        nr_cgi="5000F11000000001",
        plmn= "006496F2",
        tac= "000001",
        timestamp=hex_timestamp
    )

    return KSEAF, ngap_uplink_message.to_hex()+authentication_response_message.to_hex()


def test():
    # 示例数据
    ngap_request_message_hex = "0004403e000003000a000200020055000200010026002b2a7e005601020000216b0bbf58144c8d74ade24b5626bd5d2f2010719762a4686f80005ec4e5f58c90a204"
    # ngap_response_message_hex = "002E4040000004000A0002000200550002000100260016157E00572D106A9EF8FC9D2C11A36D4DA18229C3B925007940135000F110000000010000F110000001EB5DA5BA"
    "0004403e000003000a000200020055000200010026002b2a7e005601020000216b0bbf58144c8d74ade24b5626bd5d2f2010719762a4686f80005ec4e5f58c90a204"
    "002E4040000004000A0002000200550002000100260016157E00572D106A9EF8FC9D2C11A36D4DA18229C3B925007940135000F110000000010000F110000001EB5DA5BA"
    "002E4040000004000A000220027F00550002000500260016157E00572D103A950EF2EF83A14278170C12B143CD7F007940135000F110000000010000F11000000167FFBD8F"
    # 拆分 NGAP 头部和 NAS-PDU
    ngap_response_message_hex = authReceiveAndResult(ngap_request_message_hex)

    # 打印结果
    print(f"ngap_response_message_hex: {ngap_response_message_hex}")



if __name__ == "__main__":
    test()