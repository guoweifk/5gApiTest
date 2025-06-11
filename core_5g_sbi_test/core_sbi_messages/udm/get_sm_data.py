#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-03 22:44 
@file: getSmDataRequest.py
@project: 5gAPItest
@describe: Powered By GW
"""
from core_5g_sbi_test.core_sbi_messages.sbi_base_processor import SBIBaseProcessor
import json


class GetSMDataProcessor(SBIBaseProcessor):
    def __init__(self, connection, ):
        super().__init__(connection)


    def sender(self):
        return "SMF"

    def receiver(self):
        return "UDM"

    # ========= Client 使用 =========
    def build_headers(self, body=None):
        return [
            (':method', 'GET'),
            (':path', '/nudm-sdm/v2/imsi-001010000000000/sm-data'
                      '?single-nssai=%7B%22sst%22%3A1%7D'
                      '&dnn=internet'
                      '&plmn-id=%7B%22mcc%22%3A%22001%22%2C%22mnc%22%3A%2201%22%7D'),
            (':scheme', 'http'),
            (':authority', f'{self.connection.host}:{self.connection.port}'),
            ('accept', 'application/json,application/problem+json'),
            ('3gpp-sbi-sender-timestamp', 'Tue, 03 Jun 2025 02:41:42.998 GMT'),
            ('3gpp-sbi-max-rsp-time', '10000'),
            ('user-agent', 'SMF')
        ]

    def build_body(self):
        return b''  # GET 请求无 body


    # ========= Server 使用 =========
    def match(self, path: str) -> bool:
        # 支持变量 IMSI，可使用前缀匹配判断是否是 sm-data 请求
        return path.startswith("/nudm-sdm/v2/imsi-") and "/sm-data" in path

    def handle(self, stream_id: int, conn, headers: list) -> tuple:
        # 1. 构造响应头
        response_headers = [
            (':status', '200'),
            ('server', 'Open5GS v2.7.5-5-g1182a99'),
            ('date', 'Tue, 03 Jun 2025 02:41:43 GMT'),
            ('content-type', 'application/json'),
        ]

        # 2. 构造响应体
        body_dict = [
            {
                "singleNssai": {"sst": 1},
                "dnnConfigurations": {
                    "internet": {
                        "pduSessionTypes": {
                            "defaultSessionType": "IPV4V6",
                            "allowedSessionTypes": ["IPV4", "IPV6", "IPV4V6"]
                        },
                        "sscModes": {
                            "defaultSscMode": "SSC_MODE_1",
                            "allowedSscModes": ["SSC_MODE_1", "SSC_MODE_2", "SSC_MODE_3"]
                        },
                        "5gQosProfile": {
                            "5qi": 9,
                            "arp": {
                                "priorityLevel": 8,
                                "preemptCap": "NOT_PREEMPT",
                                "preemptVuln": "NOT_PREEMPTABLE"
                            },
                            "priorityLevel": 8
                        },
                        "sessionAmbr": {
                            "uplink": "1000000 Kbps",
                            "downlink": "1000000 Kbps"
                        }
                    }
                }
            }
        ]

        # 3. 编码 JSON 并设置 content-length
        body_bytes = json.dumps(body_dict).encode('utf-8')
        response_headers.append(('content-length', str(len(body_bytes))))

        # 4. 返回 header 和 body 给 dispatcher 或 conn 层统一发送
        return response_headers, body_bytes

