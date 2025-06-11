#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-03 23:20 
@file: get_am_data.py
@project: 5gAPItest
@describe: Powered By GW
"""

from core_5g_sbi_test.core_sbi_messages.sbi_base_processor import SBIBaseProcessor
from core_5g_sbi_test.sbi_constant import constants

import json
from email.utils import formatdate


class GetAmDataProcessor(SBIBaseProcessor):
    def __init__(self, connection, ):
        super().__init__(connection)

    def sender(self):
        return "AMF"

    def receiver(self):
        return "UDM"

    def build_headers(self, body=None):
        encoded_plmn = "%7B%22mcc%22%3A%22001%22%2C%22mnc%22%3A%2201%22%7D"
        path = f"/nudm-sdm/v2/{constants.IMSI}/am-data?plmn-id={encoded_plmn}"
        return [
            (':method', 'GET'),
            (':path', path),
            (':scheme', 'http'),
            (':authority', f"{self.connection.host}:{self.connection.port}"),
            ('accept', 'application/json,application/problem+json'),
            ('3gpp-sbi-sender-timestamp', 'Tue, 03 Jun 2025 02:41:42.766 GMT'),
            ('3gpp-sbi-max-rsp-time', '10000'),
            ('user-agent', 'AMF')
        ]

    def build_body(self):
        return b''

    def match(self, path: str) -> bool:
        return path.startswith("/nudm-sdm/v2/imsi-") and path.endswith("/am-data")

    def handle(self, stream_id, conn, headers: list):
        response_headers = [
            (':status', '200'),
            ('server', 'Open5GS v2.7.5-5-g1182a99'),
            ('date', formatdate(timeval=None, localtime=False, usegmt=True)),
            ('content-type', 'application/json'),
        ]

        response_body_dict = {
            "subscribedUeAmbr": {
                "uplink": "1000000 Kbps",
                "downlink": "1000000 Kbps"
            },
            "nssai": {
                "defaultSingleNssais": [
                    {"sst": 1}
                ]
            }
        }

        response_body = json.dumps(response_body_dict).encode("utf-8")
        response_headers.append(('content-length', str(len(response_body))))

        return response_headers, response_body
