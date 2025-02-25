#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-19 11:33 
@file: securityReceiveResult.py
@project: 5gAPItest
@describe: Powered By GW
"""
# 安全的信息调用这个pycrate_mobile 中
from message import *
import time
from  pycrate_mobile  import *
from pycrate_mobile.NAS5G import parse_NAS5G




def securityReceiveAndResult(security_request:bytes):
    ngap_header, nas_pdu = split_ngap_nas(security_request)
    ngap_downlink_message = NGAPDownLinkTransportNASMessage.parse(ngap_header)
    # 转换为十六进制格式（大写）
    current_timestamp = int(time.time())
    hex_timestamp = format(current_timestamp, 'X')
    ngap_uplink_message = NGAPUplinkTransportNASMessage(
        amf_ue_ngap_id=ngap_downlink_message.amf_ue_ngap_id,
        ran_ue_ngap_id=ngap_downlink_message.ran_ue_ngap_id,
        nas_pdu_type="003d",
        nas_pdu_length="3c",
        ngap_message_len = "67"
    )

    # security_request_message = AuthenticationRequestMessage.parse(nas_pdu)
    # print(ngap_downlink_message)
    # print(security_request_message)

    security_response_message = "7e04f15f1642007e005e7700094573806121856151f17100237e004179000d0100f1100000000000000000001001002e04f0f0f0f02f020101530100007940135000f110000000010000f110000001eb5da5ba"

    return ngap_uplink_message.to_hex()+security_response_message

def test():
    # 假设 nas_message 是一个包含 5G NAS 消息的字节对象
    nas_message = "7e0323b43810007e005d020304f0f0f0f0e1360102"  # 示例字节流

    # 调用 parse_NAS5G 函数解析消息
    parsed_message, error_code = parse_NAS5G(bytes.fromhex(nas_message))

    if error_code == 0:
        print("解析成功:")
        print(parsed_message)
    else:
        print(f"解析失败，错误码: {error_code}")

if __name__ == "__main__":
    test()