#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-19 11:33 
@file: securityReceiveResult.py
@project: 5gAPItest
@describe: Powered By GW
"""
from message import *
import time

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
    print(ngap_downlink_message)
    # print(security_request_message)

    security_response_message = "7e04f15f1642007e005e7700094573806121856151f17100237e004179000d0100f1100000000000000000001001002e04f0f0f0f02f020101530100007940135000f110000000010000f110000001eb5da5ba"

    return ngap_uplink_message.to_hex()+security_response_message