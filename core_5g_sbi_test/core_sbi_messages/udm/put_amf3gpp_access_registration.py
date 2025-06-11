#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-03 22:23 
@file: PutAmf3gppAccessRegistrationProcessor.py
@project: 5gAPItest
@describe: Powered By GW
"""

from core_5g_sbi_test.core_sbi_messages.sbi_base_processor import SBIBaseProcessor
from core_5g_sbi_test.sbi_constant import constants
import json
from email.utils import formatdate


class PutAmf3gppAccessRegistrationProcessor(SBIBaseProcessor):
    def __init__(self, connection, ):
        super().__init__(connection)

    def sender(self):
        return "AMF"

    def receiver(self):
        return "UDM"

    def build_headers(self, body):
        return [
            (':method', 'PUT'),
            (':path', F'/nudm-uecm/v1/{constants.IMSI}/registrations/amf-3gpp-access'),
            (':scheme', 'http'),
            (':authority', f'{self.connection.host}:{self.connection.port}'),
            ('content-type', 'application/json'),
            ('accept', 'application/json,application/problem+json'),
            ('content-length', str(len(body))),  # 实际长度会自动设置，这里可省略
            ('3gpp-sbi-sender-timestamp', 'Tue, 03 Jun 2025 02:41:42.760 GMT'),
            ('3gpp-sbi-max-rsp-time', '10000'),
            ('user-agent', 'AMF')
        ]

    def build_body(self):
        body = {
            "amfInstanceId": constants.AMF_INSTANCE_ID,
            "pei": constants.PEI,
            "deregCallbackUri": f"http://{constants.AMF_IP}/namf-callback/v1/{constants.IMSI}/dereg-notify",
            "initialRegistrationInd": True,
            "guami": constants.GUAMI,
            "ratType": constants.RAT_TYPE
        }
        return json.dumps(body).encode("utf-8")

    def match(self, path: str) -> bool:
        return (
            path.startswith("/nudm-uecm/v1/imsi-")
            and path.endswith("/registrations/amf-3gpp-access")
        )


    def handle(self, stream_id, conn, headers: list, request_body: bytes = b''):
        # 回显请求体作为响应体
        response_body = request_body or b'{}'

        response_headers = [
            (':status', '200'),
            ('server', 'Open5GS v2.7.5-5-g1182a99'),
            ('date', formatdate(timeval=None, localtime=False, usegmt=True)),
            ('content-type', 'application/json'),
            ('content-length', str(len(response_body))),
        ]

        return response_headers, response_body
