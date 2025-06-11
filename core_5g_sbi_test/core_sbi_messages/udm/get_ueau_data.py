#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-04 19:21 
@file: get_ueau_data.py
@project: 5gAPItest
@describe: Powered By GW
"""
from core_5g_sbi_test.core_sbi_messages.sbi_base_processor import SBIBaseProcessor
from core_5g_sbi_test.sbi_constant import constants
import json
from email.utils import formatdate
import time

class PostAuthDataProcessor(SBIBaseProcessor):
    def __init__(self, connection, ):
        super().__init__(connection)

    def sender(self):
        return "AUSF"

    def receiver(self):
        return "UDM"

    def build_headers(self, body: dict):
        return [
            (":method", "POST"),
            (":path", "/nudm-ueau/v1/suci-0-001-01-0000-0-0-0000000000/security-information/generate-auth-data"),
            (":scheme", "http"),
            (":authority", "127.0.0.12:7777"),
            ("content-type", "application/json"),
            ("accept", "application/json,application/problem+json"),
            ("content-length", str(len(json.dumps(body).encode('utf-8')))),
            ("user-agent", "AUSF"),
            ("3gpp-sbi-sender-timestamp", time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())),
            ("3gpp-sbi-max-rsp-time", "10000")
        ]

    def build_body(self):
        return {
            "servingNetworkName": "5G:mnc001.mcc001.3gppnetwork.org",
            "ausfInstanceId": "3b53fc50-4024-41f0-a199-23268a305fb0"
        }

    def match(self, path: str) -> bool:
        return (
                path.startswith("/nudm-ueau/v1")
                and path.endswith("/security-information/generate-auth-data")
        )



    def handle(self, stream_id, conn, headers: list, request_body: bytes = b''):
        response_body = {
            "authType": "5G_AKA",
            "authenticationVector": {
                "avType": "5G_HE_AKA",
                "rand": "16bbf88766468dea5871c244e3618b0d",
                "autn": "374ebb2dcb018000777ba66c58ccf3dc",
                "xresStar": "0deaf60b6d0b6ffa764eb869492d8315",
                "kausf": "8becc1f81a7de05bcd89cce676a1cdcf11f872d3ae842a05386a971a26ce2fc7"
            },
            "supi": "imsi-001010000000000"
        }

        response_bytes = json.dumps(response_body).encode('utf-8')

        response_headers = [
            (":status", "200"),
            ("server", "Open5GS v2.7.5-5-g1182a99"),
            ("date", time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())),
            ("content-type", "application/json"),
            ("content-length", str(len(response_bytes)))
        ]
        return response_headers, response_body
